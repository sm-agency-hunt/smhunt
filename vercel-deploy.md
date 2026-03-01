# Deploying SMHunt to Vercel

This document explains how to deploy the SMHunt application to Vercel.

## Prerequisites

1. Install the Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Log in to your Vercel account:
   ```bash
   vercel login
   ```

## Environment Variables

Before deploying, you'll need to set up the following environment variables in your Vercel project:

### Required Variables
- `VERCEL=1` - Indicates the app is running in Vercel environment
- `DATABASE_URL` - Your PostgreSQL database connection string (for production)
- `SECRET_KEY` - Secret key for JWT tokens
- `FRONTEND_URL` - URL of your frontend application

### Optional Variables
- `DEBUG=False` - Set to "False" for production
- `LOG_LEVEL=INFO` - Logging level
- `OPENAI_API_KEY` - OpenAI API key (if using OpenAI)
- `ANTHROPIC_API_KEY` - Anthropic API key (if using Claude)
- `SENDGRID_API_KEY` - SendGrid API key (if sending emails)
- `GOOGLE_MAPS_API_KEY` - Google Maps API key (if using location services)

## Deployment Steps

1. Navigate to your project directory:
   ```bash
   cd your-smhunt-project-directory
   ```

2. Deploy to Vercel:
   ```bash
   vercel --prod
   ```

3. During the first deployment, you'll be prompted to:
   - Link to an existing project or create a new one
   - Set environment variables
   - Configure build settings

## Important Notes

- The application has been modified to work in serverless environments like Vercel
- Database initialization is skipped in Vercel environment (VERCEL=1)
- Health checks adapt to serverless environment
- The application uses the `mangum` adapter to work with Vercel's serverless functions

## Troubleshooting

If you encounter issues:

1. Check that all required environment variables are set in Vercel dashboard
2. Ensure your `vercel.json` file is present in the root directory
3. Verify that the Python version in `runtime.txt` is compatible with Vercel
4. Check Vercel logs for detailed error messages

## Local Testing

To test locally in Vercel-like environment:

```bash
export VERCEL=1
python main.py
```

Then visit `http://localhost:8000` to verify the application works correctly.