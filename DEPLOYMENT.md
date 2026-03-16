# Deployment Guide

## Production Deployment

### Prerequisites
- Docker & Docker Compose
- PostgreSQL 13+
- Redis 6+
- Ollama instance

### Environment Setup

Create `.env.production`:
```bash
DATABASE_URL=postgresql://user:password@db:5432/credit_tracker
REDIS_URL=redis://cache:6379/0
WHISPER_DEVICE=cuda  # or cpu
WHISPER_COMPUTE_TYPE=float32
OLLAMA_MODEL=mistral
APP_ENV=production
```

### Docker Deployment

1. **Build image:**
   ```bash
   docker build -t credit-tracker-api:latest .
   ```

2. **Run with docker-compose:**
   ```bash
   docker-compose up -d
   ```

3. **Verify health:**
   ```bash
   curl http://localhost:8000/health
   ```

### Database Migrations

```bash
# Inside container
docker-compose exec api alembic upgrade head
```

### Monitoring

```bash
# View logs
docker-compose logs -f api

# Check resource usage
docker stats credit-tracker-api

# Health check every 30s
watch -n 30 'curl -s http://localhost:8000/health'
```

### Scaling

```bash
# Scale API replicas
docker-compose up -d --scale api=3

# Configure load balancer (nginx)
```

### Backup and Recovery

```bash
# Backup database
pg_dump credit_tracker > backup.sql

# Restore
psql credit_tracker < backup.sql
```

## Monitoring and Logging

### Key Metrics to Track
- Voice transaction success rate
- Average parsing latency
- Whisper model load time
- Database query performance
- API error rates

### Alerting Rules
- Parsing failure rate > 5%
- API latency > 5 seconds
- Database connections > 80%
- Ollama unavailable

## Security Checklist

- [ ] Enable HTTPS (SSL/TLS)
- [ ] Configure CORS properly
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (SQLAlchemy)
- [ ] CSRF tokens on forms
- [ ] Secure password hashing (bcrypt)
- [ ] Database encryption at rest
- [ ] Audit logging enabled

## Disaster Recovery

### RTO/RPO Targets
- RTO (Recovery Time Objective): 1 hour
- RPO (Recovery Point Objective): 15 minutes

### Backup Strategy
- Daily database backups
- Weekly full backups to S3
- Model cache cached locally
- Configuration backed up to Git

### Failover Procedure
1. Stop primary API
2. Promote standby database
3. Reconfigure DNS
4. Run smoke tests
5. Monitor error rates
