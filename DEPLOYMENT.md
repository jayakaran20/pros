# Deployment Guide — Cropfit

This guide provides end-to-end instructions for deploying the **Cropfit** platform to production cloud environments.

---

## 1. Cloud Deployment with Render (Recommended)

Cropfit includes a production-ready Infrastructure-as-Code blueprint ([`render.yaml`](file:///C:/Users/TICKMARKS/OneDrive%20-%20tickmarks.net/Desktop/Cropfit/render.yaml)) configured for Render.

### Deployment Steps:
1. Log in to [Render](https://render.com) and connect your GitHub account.
2. Click **New +** $\rightarrow$ **Blueprint**.
3. Select the repository: **`jayakaran20/pros`**.
4. Render will automatically parse `render.yaml` and provision:
   * **`cropfit-backend`**: Dockerized FastAPI service with a 1 GB SSD persistent volume mounted at `/app/data`.
   * **`cropfit-frontend`**: Dockerized React + Vite SPA served via Nginx reverse proxy.
5. Click **Apply Blueprint** to initiate the build.
6. Once deployed, run the automated smoke test against your live domain:
   ```bash
   python backend/scripts/smoke_test.py --base-url https://cropfit-backend.onrender.com
   ```

---

## 2. Self-Hosted Deployment with Docker Compose

To deploy on any virtual private server (VPS) such as AWS EC2, DigitalOcean Droplet, or Linode:

### Prerequisites:
* Docker Engine 24+ and Docker Compose v2 installed.

### Steps:
```bash
# 1. Clone repository
git clone https://github.com/jayakaran20/pros.git /opt/cropfit
cd /opt/cropfit

# 2. Build and run containers detached in background
docker compose up -d --build

# 3. Verify health checks
docker compose ps
curl -f http://localhost:8000/api/v1/health

# 4. View real-time aggregated logs
docker compose logs -f
```

---

## 3. Environment Variable Reference

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `PYTHONUNBUFFERED` | `1` | Forces unbuffered stdout/stderr streams for container logging |
| `LOG_LEVEL` | `INFO` | Logging threshold (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `DATABASE_URL` | `sqlite:////app/data/cropfit.db` | Target database connection URI |
| `MODELS_DIR` | `/app/ml_experiments/models` | Filesystem path where model artifacts reside |
| `CORS_ORIGINS` | `*` | Comma-separated list of permitted origin domains |
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000/api/v1` | Base URL used by the client to communicate with the API |
