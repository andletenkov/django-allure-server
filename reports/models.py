import distutils.dir_util
import os
import pathlib
import shutil
import uuid
from collections import Iterable
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.generics import get_object_or_404
from .tasks import generate_report_task

from results.models import AllureResult

join = os.path.join


class AllureReport(models.Model):
    path = models.JSONField()
    report = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        if not self.report:
            raise RuntimeError('Report need to be generated first before accessing its "url" property')
        return self.report.url

    @classmethod
    def generate(cls, results_id, copy_history=True, *args, **kwargs):
        instance = cls(*args, **kwargs)
        results = get_object_or_404(AllureResult, pk=results_id).unzip()
        report_dir = instance._new_report_dir()

        if copy_history:
            instance._copy_history(results)

        index_page = join(report_dir, 'index.html')
        instance.report = os.path.relpath(index_page, start=settings.MEDIA_ROOT)
        instance.save()

        generate_report_task.delay(results, report_dir)
        return instance

    def _require_path(self):
        if not self.path:
            raise RuntimeError('Report "path" need to be specified first')

    def _new_report_dir(self):
        self._require_path()

        uid = str(uuid.uuid4())
        base_dir = 'reports'

        assert isinstance(self.path, Iterable), \
            f"Report path should be an iterable, but got: {type(self.path)}"

        return join(
            settings.MEDIA_ROOT,
            base_dir,
            *self.path,
            uid
        )

    def _copy_history(self, copy_to):
        self._require_path()

        last_report_query = self.__class__.objects.filter(path=self.path).order_by('-created_at')[:1]

        if last_report_query.exists():
            last_report = last_report_query.get()
            history_dir = join(pathlib.Path(last_report.report.path).parent.absolute(), 'history')

            if os.path.isdir(history_dir):
                distutils.dir_util.copy_tree(
                    join(history_dir),
                    join(copy_to, 'history')
                )


@receiver(post_delete, sender=AllureReport)
def delete_allure_report_hook(sender, instance, using, **kwargs):
    if instance.report:
        report_dir = pathlib.Path(instance.report.path).parent.absolute()
        if os.path.isdir(report_dir):
            shutil.rmtree(report_dir)

            # remove empty parent dirs
            parent_dir = report_dir.parent.absolute()
            while True:
                if os.listdir(parent_dir):
                    break
                else:
                    os.rmdir(parent_dir)
                    parent_dir = parent_dir.parent.absolute()
