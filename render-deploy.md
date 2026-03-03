# Render Deployment Guide

This guide explains how to deploy the SMHunt backend to Render.

## Prerequisites

1. A Render account (https://render.com)
2. A PostgreSQL database (can be provisioned on Render or external)
3. Git repository with your code

## Deployment Steps

### 1. Create Render Services

1. Go to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:

**Service Settings:**
- **Name**: smhunt-backend
- **Region**: Choose your preferred region
- **Branch**: main (or your deployment branch)
- **Root Directory**: / (root of repository)

**Build Settings:**
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

### 2. Configure Environment Variables

In your Render service settings, add these environment variables:

**Required Variables:**
- `DATABASE_URL` - Your PostgreSQL database connection string
- `SECRET_KEY` - A strong secret key for JWT tokens
- `DEBUG` - Set to "False" for production

**Optional Variables:**
- `LOG_LEVEL` - "INFO" (default) or "DEBUG"
- `REDIS_URL` - If using Redis for caching/Celery
- `OPENAI_API_KEY` - If using OpenAI services
- `ANTHROPIC_API_KEY` - If using Anthropic services
- Any other API keys you need

### 3. Database Setup

You can either:
1. **Use Render's PostgreSQL** - Provision a database from Render dashboard
2. **Use External Database** - Connect to your own PostgreSQL instance

For Render PostgreSQL:
1. Create a new "PostgreSQL" service in Render
2. Note the connection string provided
3. Add it as `DATABASE_URL` in your web service environment variables

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues

## Configuration Notes

### Database Connection
The application uses `DATABASE_URL` environment variable for database connection:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

Make sure your `DATABASE_URL` follows the format:
```
postgresql://username:password@host:port/database_name
```

### Port Configuration
Render automatically sets the `PORT` environment variable. The application will use this port for the Uvicorn server.

### Health Checks
The application includes a `/health` endpoint that Render can use for health checks.

## Troubleshooting

### Common Issues

1. **Build Failures**: Check that all dependencies in `requirements.txt` are compatible
2. **Database Connection**: Verify `DATABASE_URL` format and credentials
3. **Startup Issues**: Check logs for missing environment variables
4. **Memory Issues**: Monitor resource usage in Render dashboard

### Environment Variables Check
Ensure these critical variables are set:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Strong secret key
- `DEBUG=False` - Production mode

## Migration from Railway

If you're migrating from Railway:
1. All Railway-specific configurations have been removed
2. The application now uses standard environment variables
3. Database connection uses `DATABASE_URL` (no Railway-specific variables)
4. No hardcoded Railway URLs or configurations remain

## Support

For issues with the application:
1. Check Render logs for error messages
2. Verify all environment variables are correctly set
3. Ensure database connectivity
4. Test locally with the same configuration

The application is now fully compatible with Render deployment and follows standard Python web application practices.