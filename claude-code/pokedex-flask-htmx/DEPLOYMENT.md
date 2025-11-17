# Deployment Guide

This guide covers deploying the Pokédex application to production.

## Docker Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+

### Steps

1. Clone the repository:
```bash
git clone <repo-url>
cd pokedex-flask-htmx
```

2. Set environment variables:
```bash
# Create .env file
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" > .env
echo "FLASK_ENV=production" >> .env
```

3. Build and start:
```bash
docker-compose up -d --build
```

4. Verify deployment:
```bash
docker-compose ps
curl http://localhost:5000
```

5. View logs:
```bash
docker-compose logs -f
```

6. Stop application:
```bash
docker-compose down
```

## Production Considerations

### Security

1. **Secret Key**: Always use a strong, random secret key:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

2. **HTTPS**: Use a reverse proxy (nginx, Caddy) for HTTPS

3. **Environment Variables**: Never commit `.env` files

### Performance

1. **Caching**: Consider adding Redis for API response caching

2. **CDN**: Serve static assets via CDN in production

3. **Gunicorn**: Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Monitoring

1. **Logging**: Configure structured logging

2. **Health Checks**: Add `/health` endpoint

3. **Metrics**: Consider Prometheus + Grafana

## Cloud Platforms

### Deploy to Railway

1. Install Railway CLI
2. Run `railway init`
3. Run `railway up`

### Deploy to Render

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python run.py`

### Deploy to Heroku

1. Create `Procfile`:
```
web: gunicorn "app:create_app()"
```

2. Deploy:
```bash
heroku create
git push heroku main
```

## Environment Variables for Production

```
FLASK_ENV=production
SECRET_KEY=<your-secret-key>
PORT=5000
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs web
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8080:5000"
```

### API rate limiting
PokeAPI has rate limits. Consider implementing caching for production use.
