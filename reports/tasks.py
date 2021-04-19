import os
import sh
from allure_server import celery_app


@celery_app.task(bind=True)
def generate_report_task(self, results_dir, report_dir):
    if not os.path.isdir(results_dir):
        raise ValueError(f'Failed to find allure results folder: {results_dir}')

    out = str(sh.allure('generate', results_dir, '-o', report_dir, '--clean'))

    if not out.startswith(f'Report successfully generated to {report_dir}'):
        raise RuntimeError(f'Generate report error: {str(out)}')

    return out
