# 📶 VPS Monitor Premium

Um monitor de sistema leve, moderno e elegante para servidores Linux (VPS), desenvolvido para oferecer métricas em tempo real com uma interface premium.

## 🚀 Funcionalidades

-   **⚡ CPU Real:** Monitoramento de uso ativo, total e I/O Wait (Atraso).
-   **🧠 Memória RAM:** Visualização em tempo real do uso, total e disponibilidade.
-   **💾 Disco SSD:** Status de armazenamento consumido e uptime do sistema.
-   **🌐 Tráfego de Rede:** Monitoramento de entrada (⬇️) e saída (⬆️) em tempo real.
-   **📡 Transferência Acumulada:** Contador total de dados transmitidos em GB.
-   **⏲️ Uptime & Load:** Acompanhamento da estabilidade e carga média do servidor.

## 🛠️ Tecnologias

-   **Backend:** Python 3.12 (Baseado em `http.server` para máxima leveza e zero dependências externas).
-   **Frontend:** HTML5, CSS3 (Glassmorphism & Luminous Design), JavaScript Vanilla.
-   **Container:** Docker & Docker Compose para fácil implantação.
-   **OS:** Otimizado para ler métricas diretamente do `/proc` do Linux.

## 📦 Como Instalar

### 1. Requisitos
-   Docker instalado no servidor.
-   Docker Compose instalado.

### 2. Clonar o repositório
```bash
git clone https://github.com/LelloTereciani/vps-monitor.git
cd vps-monitor
```

### 3. Iniciar o Monitor
```bash
docker-compose up -d --build
```

O painel estará disponível no navegador através do endereço: `http://ip-do-seu-servidor:9090`

## 🎨 Interface
A interface foi desenhada com foco em **Visual Excellence**, utilizando:
-   **Tipografia:** Inter e JetBrains Mono.
-   **Estética:** Dark Mode com efeitos de transparência (Glassmorphism).
-   **UX:** Micro-animações de pulso e barras de progresso dinâmicas.

---
🚀 Desenvolvido por [Lello Tereciani](https://github.com/LelloTereciani)
