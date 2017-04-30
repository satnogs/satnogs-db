import csv

from celery.task import task
from orbit import satellite

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from db.base.models import Satellite, DemodData


@task(ignore_result=False)
def check_celery():
    """Dummy celery task to check that everything runs smoothly."""
    pass


@task(ignore_result=True)
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


@task
def export_frames(norad, email, uid):
    """Task to export satellite frames in csv."""
    frames = DemodData.objects.filter(satellite__norad_cat_id=norad)
    filename = '{0}-{1}.csv'.format(norad, uid)
    filepath = '{0}/download/{1}'.format(settings.MEDIA_ROOT, filename)
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        for obj in frames:
            writer.writerow([obj.timestamp, obj.display_frame()])

    # Notify user
    subject = '[satnogs] Your request for exported frames is ready!'
    template = 'emails/exported_frames.txt'
    data = {
        'url': '{0}{1}{2}.csv'.format(settings.SITE_URL, settings.MEDIA_URL, filename),
        'norad': norad
    }
    message = render_to_string(template, {'data': data})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], False)
