import os
import shutil
from zipfile import ZipFile

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class AllureResult(models.Model):
    results = models.FileField(upload_to='results/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.results.name

    @property
    def extract_dir(self):
        return self.results.path.rsplit('.', 1)[0]

    def unzip(self):
        extract_to = self.extract_dir
        with ZipFile(self.results.path, 'r') as zip_file:
            zip_file.extractall(extract_to)
        return extract_to


@receiver(post_delete, sender=AllureResult)
def delete_allure_results_hook(sender, instance, using, **kwargs):
    if instance.results:
        if os.path.isfile(instance.results.path):
            os.remove(instance.results.path)

            # remove corresponding unzipped results
            if os.path.isdir(instance.extract_dir):
                shutil.rmtree(instance.extract_dir)
