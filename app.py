#!/usr/bin/env python3
"""
VPS Monitor API v1.5 — Correções Críticas de Dados (Disco e Rede)
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, subprocess, re, os, time

# Globais persistentes de estado
cpu_last = {"total": 0, "idle": 0, "iowait": 0}
net_last = {"rx": 0, "tx": 0, "time": time.time()}

def get_real_cpu():
    global cpu_last
    try:
        with open("/proc/stat", "r") as f:
            l = f.readline().split()
        if not l or l[0] != "cpu": return 0.0, 0.0, 0.0
        v = [int(x) for x in l[1:9]]
        total = sum(v); idle = v[3]; iowait = v[4]
        dt = total - cpu_last["total"]; di = idle - cpu_last["idle"]; dw = iowait - cpu_last["iowait"]
        cpu_last = {"total": total, "idle": idle, "iowait": iowait}
        if dt == 0: return 0.0, 0.0, 0.0
        active_usage = round((dt - di - dw) / dt * 100, 1)
        wait_usage = round(dw / dt * 100, 1)
        total_usage = round((dt - di) / dt * 100, 1)
        return active_usage, wait_usage, total_usage
    except Exception: return 0.0, 0.0, 0.0

def get_net_delta():
    global net_last
    try:
        rx, tx = 0, 0
        with open("/proc/net/dev") as f:
            for l in f:
                if "eth0" in l:
                    p = l.split(); rx, tx = int(p[1]), int(p[9]); break
        now = time.time()
        if net_last["rx"] == 0:
            net_last = {"rx": rx, "tx": tx, "time": now}
            return 0.0, 0.0, rx, tx
        dr, dt = (rx - net_last["rx"]) / 1024**2, (tx - net_last["tx"]) / 1024**2
        net_last = {"rx": rx, "tx": tx, "time": now}
        return round(dr, 1), round(dt, 1), rx, tx
    except: return 0.0, 0.0, 0, 0

def get_metrics():
    m = {}
    
    # CPU
    a, w, t = get_real_cpu()
    m["cpu_active"] = a; m["cpu_wait"] = w; m["cpu_total"] = t; m["cpu_percent"] = a
    
    # Memória
    try:
        with open("/proc/meminfo") as f:
            mem = {l.split(":")[0]: int(l.split(":")[1].split()[0]) for l in f.readlines()[:10]}
        tot, av = mem["MemTotal"], mem["MemAvailable"]
        usd = tot - av
        m["mem_total_mb"] = round(tot / 1024); m["mem_used_mb"] = round(usd / 1024)
        m["mem_percent"] = round(usd / tot * 100, 1)
    except: m["mem_percent"] = 0

    # Disco (Parsing robusto usando float)
    try:
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        # Ex: Filesystem Size Used Avail Use% Mounted on
        #     /dev/sda1  48G  7.9G  40G  17% /
        row = r.stdout.splitlines()[1].split()
        def parse_gb(s): return float(re.sub(r'[^0-9.]', '', s))
        m["disk_total_gb"] = round(parse_gb(row[1]))
        m["disk_used_gb"] = round(parse_gb(row[2]), 1)
        m["disk_percent"] = round(m["disk_used_gb"] / m["disk_total_gb"] * 100, 1)
    except Exception as e:
        print(f"Erro disco: {e}")
        pass

    # Rede
    dr, dt, ar, at = get_net_delta()
    # Usamos o acumulado em GB se o diferencial for muito baixo no ciclo curto?
    # Não, o usuário quer ver o "2.2 MB / 1.4 MB" que batia com o painel dele.
    # Provavelmente o painel dele mostra média do minuto ou dia. 
    # Vou manter o delta mas com precisão de uma casa decimal.
    m["net_rx_mb"] = dr; m["net_tx_mb"] = dt
    m["net_rx_total_gb"] = round(ar / 1024**3, 2); m["net_tx_total_gb"] = round(at / 1024**3, 2)

    # Uptime e Load
    try:
        with open("/proc/uptime") as f: s = float(f.read().split()[0])
        m["uptime"] = f"{int(s // 86400)}d {int((s % 86400) // 3600)}h {int((s % 3600) // 60)}m"
        p = open("/proc/loadavg").read().split()
        m["load_1"], m["load_5"], m["load_15"] = float(p[0]), float(p[1]), float(p[2])
    except: m["uptime"] = "N/A"
    
    m["timestamp"] = int(time.time())
    return m

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/metrics", "/metrics/"):
            self.send_response(404); self.end_headers(); return
        m = get_metrics()
        body = json.dumps(m).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args): pass

if __name__ == "__main__":
    get_real_cpu(); get_net_delta()
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", 9090))), Handler).serve_forever()
