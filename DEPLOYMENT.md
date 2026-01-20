# Production Deployment Guide

## 1. Server Requirements
- Ubuntu 22.04+
- Docker & Docker Compose
- Domain name pointing to server IP

## 2. Setup
```bash
git clone <your-repo> /var/www/codein
cd /var/www/codein
cp backend/.env.example backend/.env
docker-compose up -d postgres backend nginx
```

## 3. SSL (First Run)
```bash
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot   -d example.com -d www.example.com   --email admin@example.com --agree-tos --no-eff-email
docker-compose restart nginx
```

## 4. GitHub Secrets
- SERVER_HOST
- SERVER_USER
- SERVER_SSH_KEY

Push to `main` to auto-deploy 🚀
