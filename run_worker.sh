#!/bin/sh

# Starting celery worker
#celery -A allure_server worker -l info --logfile="worker.log"
celery -A allure_server worker -l info