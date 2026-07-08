from celery import shared_task
from django.core.management import call_command


@shared_task
def run_api_test():
    call_command("test_api",
    username='test1',
    password='supersecret')