import csv
from datetime import datetime, timedelta

from orbit import satellite

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from db.base.models import Satellite, DemodData
from db.celery import app


@app.task(task_ignore_result=False)
def check_celery():
    """Dummy celery task to check that everything runs smoothly."""
    pass


@app.task
def update_all_tle():
    """Task to update all satellite TLEs"""
    satellites = Satellite.objects.all()

    for obj in satellites:
        try:
            sat = satellite(obj.norad_cat_id)
        except:
            continue

        tle = sat.tle()
        obj.tle1 = tle[1]
        obj.tle2 = tle[2]
        obj.save()


@app.task
def export_frames(norad, email, uid, period=None):
    """Task to export satellite frames in csv."""
    now = datetime.utcnow()
    if period:
        if period == '1':
            q = datetime.now() - timedelta(days=7)
            suffix = 'week'
        else:
            q = datetime.now() - timedelta(days=30)
            suffix = 'month'
        frames = DemodData.objects.filter(satellite__norad_cat_id=norad,
                                          timestamp__gte=q)
    else:
        frames = DemodData.objects.filter(satellite__norad_cat_id=norad)
        suffix = 'all'
    filename = '{0}-{1}-{2}-{3}.csv'.format(norad, uid, now.strftime('%Y%m%dT%H%M%SZ'), suffix)
    filepath = '{0}/download/{1}'.format(settings.MEDIA_ROOT, filename)
    with open(filepath, 'w') as f:
        writer = csv.writer(f, delimiter='|')
        for obj in frames:
            writer.writerow([obj.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                             obj.display_frame()])

    # Notify user
    subject = '[satnogs] Your request for exported frames is ready!'
    template = 'emails/exported_frames.txt'
    data = {
        'url': '{0}{1}download/{2}'.format(settings.SITE_URL,
                                           settings.MEDIA_URL, filename),
        'norad': norad
    }
    message = render_to_string(template, {'data': data})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], False)
