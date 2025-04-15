
---

```markdown
# 🏡 Containerized Sensors Dashboard App

![Docker Compose](https://img.shields.io/badge/Docker--Compose-Enabled-blue?logo=docker)
![Flask](https://img.shields.io/badge/Flask-App-lightgrey?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A Dockerized Sensors Dashboard application built with Flask, MySQL, and Nginx.
This stack is ideal for experimenting with a microservices-based architecture in a local or development environment.

<p align="center">
  <img src="https://raw.githubusercontent.com/yourusername/sensors_dashboard/main/screenshots/dashboard.png" alt="Smart Home Dashboard Screenshot" width="600"/>
</p>

## 📦 Stack Overview

- **Flask** – REST API and dashboard UI
- **MySQL** – Persistent data storage
- **Nginx** – Reverse proxy to Flask app
- **Docker Compose** – Orchestrates multi-container setup

---

## 🗂 Project Structure

```
.
├── app/                  # Flask application
│   ├── app.py
│   └── ...
├── nginx/
│   └── default.conf      # Nginx reverse proxy configuration
├── docker-compose.yml    # Docker Compose setup
├── screenshots/          # UI screenshots
└── README.md             # This file
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### ⚙️ Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/sensors_dashbaord.git
cd sensors_dashbaord
```

2. Start all services:

```bash
docker compose up --build
```

3. Open in your browser:

```
http://localhost
```

---

## 🔌 Services

| Service | Description       | Port (Host) |
|---------|-------------------|-------------|
| Flask   | Smart Home API/UI | `5000` (proxied by Nginx) |
| MySQL   | DB for the app    | `3306`      |
| Nginx   | Reverse proxy     | `80`        |

---

## 🐬 Database Info

Default MySQL credentials (change them in `docker-compose.yml` if needed):

- **User**: `root`
- **Password**: `rootpassword`
- **Database**: `smart_home`

---

## 🧪 Test It Out

To check that the app is working:

```bash
curl http://localhost
```

Or visit in browser: [http://localhost](http://localhost)

---

## 🧰 Docker Commands

Stop the app:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

Rebuild:

```bash
docker compose up --build
```

---

## 🐳 Docker Hub (optional)

You can pull the prebuilt image (if published):

```bash
docker pull cnshimba/sensors_dashboard
```

---

## 📸 Screenshots

| Dashboard View |
|----------------|
| ![screenshot](https://raw.githubusercontent.com/cnshimba/smart-home-system/main/screenshots/dashboard.png) |

---

## 👤 Author

**KT Nshimba**  
[@cnshimba](https://github.com/cnshimba)  
[cnshimba](https://hub.docker.com/u/cnshimba)

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

---

## 🌟 Star This Repo

If you found this useful, don’t forget to ⭐ the repo on GitHub!

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/smart-home-system.svg?style=social)](https://github.com/yourusername/smart-home-system)
```

---

