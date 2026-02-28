"""
Discovery task worker
"""
from celery import current_task
from typing import Dict


def run_discovery_task(niche: str, location: str, count: int) -> Dict:
    """
    Run business discovery task in background
    """
    # Update task progress
    current_task.update_state(
        state='PROGRESS', meta={'current': 10, 'total': 100}
    )

    # TODO: Implement actual discovery logic
    # This would typically call the discovery service

    current_task.update_state(
        state='PROGRESS', meta={'current': 100, 'total': 100}
    )

    return {
        "status": "completed",
        "niche": niche,
        "location": location,
        "discovered_count": count
    }
