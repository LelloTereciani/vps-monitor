# VPS Monitor

**Classification:** Independent Project · Study Project

A lightweight Linux VPS monitoring dashboard using Python's standard library, HTML, CSS, and vanilla JavaScript. It reads local system metrics such as CPU, memory, disk, network traffic, uptime, load, and operating-system information.

## Scope and limitations

- Designed for local and self-hosted experimentation.
- The project does not claim a commercial monitoring service, production SLA, or external security audit.
- Expose the dashboard only behind an appropriate network and authentication boundary.

## Local run

Requirements: Python 3.12+ or Docker.

```bash
python app.py
```

Or with Docker Compose:

```bash
docker compose up -d --build
```

The dashboard is normally available on port 9090. Review the Compose and Dockerfile settings before exposing it to a network.

## Technology

Python, `http.server`, HTML5, CSS3, vanilla JavaScript, Docker, and Docker Compose.

## License

MIT. See [LICENSE](LICENSE).

## Author

Lello Tereciani
