"""
SMHUNT Task Scheduler Configuration
Defines scheduled tasks for autonomous client acquisition
"""

from celery.schedules import crontab
from src.core.config import settings


# Celery Beat Schedule Configuration
CELERY_BEAT_SCHEDULE = {
    # Business Discovery Tasks - Run every hour
    'discover-new-businesses-hourly': {
        'task': 'src.tasks.celery_app.discover_businesses',
        'schedule': crontab(minute=0),  # Every hour at minute 0
        'args': ()
    },
    
    # Lead Enrichment Tasks - Run every 2 hours
    'enrich-leads-periodically': {
        'task': 'src.tasks.celery_app.enrich_leads',
        'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
        'args': ()
    },
    
    # Outreach Campaign Tasks - Run daily at 9 AM
    'send-outreach-campaigns': {
        'task': 'src.tasks.celery_app.send_outreach_campaigns',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9:00 AM
        'args': ()
    },
    
    # Follow-up Tasks - Run daily at 2 PM
    'send-follow-ups': {
        'task': 'src.tasks.celery_app.send_follow_ups',
        'schedule': crontab(hour=14, minute=0),  # Daily at 2:00 PM
        'args': ()
    },
    
    # Lead Scoring Updates - Run every 4 hours
    'update-lead-scores': {
        'task': 'src.tasks.celery_app.update_lead_scores',
        'schedule': crontab(minute=0, hour='*/4'),  # Every 4 hours
        'args': ()
    },
    
    # Analytics Reports - Run daily at midnight
    'generate-analytics-reports': {
        'task': 'src.tasks.celery_app.generate_analytics_reports',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        'args': ()
    },
    
    # Data Cleanup Tasks - Run weekly on Sunday at 3 AM
    'cleanup-old-data': {
        'task': 'src.tasks.celery_app.cleanup_old_data',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),  # Weekly Sun at 3AM
        'args': ()
    },
    
    # Health Checks - Run every 30 minutes
    'health-check-integrations': {
        'task': 'src.tasks.celery_app.health_check_integrations',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
        'args': ()
    },
    
    # Social Media Monitoring - Run every hour
    'monitor-social-media': {
        'task': 'src.tasks.celery_app.monitor_social_media',
        'schedule': crontab(minute=15),  # Every hour at 15 minutes past
        'args': ()
    },
    
    # Competitor Analysis - Run twice daily
    'analyze-competitors': {
        'task': 'src.tasks.celery_app.analyze_competitors',
        'schedule': crontab(hour='6,18', minute=0),  # Daily 6AM & 6PM
        'args': ()
    }
}


def get_celery_beat_schedule():
    """
    Returns the Celery beat schedule configuration
    Can be customized based on environment settings
    """
    schedule = CELERY_BEAT_SCHEDULE.copy()
    
    # Optionally disable certain tasks in development
    if settings.ENVIRONMENT == "development":
        # In development, we might want to run tasks less frequently
        # or with different timing
        pass
    
    return schedule


def enable_mock_scheduled_tasks(schedule_dict):
    """
    Enable mock versions of scheduled tasks for development
    This ensures the system works with mock providers during development
    """
    # When using mock providers, we might want to adjust frequencies
    # to prevent overwhelming the mock services
    if settings.ENABLE_MOCK_PROVIDERS:
        # Adjust schedules to be less aggressive with mock providers
        for task_name, task_config in schedule_dict.items():
            # For mock providers, we might want to slow down execution
            # to prevent rate limiting issues with mock services
            pass
    
    return schedule_dict