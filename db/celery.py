from __future__ import absolute_import

import os
import dotenv

from celery import Celery

dotenv.read_dotenv('./')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE'))

from django.conf import settings  # noqa

RUN_DAILY = 60 * 60 * 24

app = Celery('db')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from db.base.tasks import update_all_tle

    sender.add_periodic_task(RUN_DAILY, update_all_tle.s(),
                             name='update-all-tle')
