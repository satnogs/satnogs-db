from celery.task import task
from orbit import satellite

from db.base.models import Satellite


@task(ignore_result=False)
def check_celery():
    """Dummy celery task to check that everything runs smoothly."""
    pass


@task(ignore_result=True)
def update_all_tle():
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
