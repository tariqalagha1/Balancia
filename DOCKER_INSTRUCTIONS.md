# Docker Desktop Installation Instructions

1. Download Docker Desktop for macOS from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Open the downloaded .dmg file and drag Docker.app to Applications folder
3. Launch Docker.app from Applications
4. Once Docker is running, open Terminal and verify installation:
```bash
docker --version
docker-compose --version
```

5. Start PostgreSQL container:
```bash
cd /Users/tariq/Desktop/Balancia
docker compose up -d db
```

6. Verify PostgreSQL is running:
```bash
docker ps
```

After completing these steps, return here and we'll proceed with database migrations.