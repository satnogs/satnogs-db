from orbit import satellite

from django.core.management.base import BaseCommand

from db.base.tests import TransponderFactory
from db.base.models import Satellite


class Command(BaseCommand):
    help = 'Create initial fixtures'

    def handle(self, *args, **options):
        TransponderFactory.create_batch(20, suggestion=None, approved=True, user=None)

        satellites = Satellite.objects.all()

        for obj in satellites:
            try:
                sat = satellite(obj.norad_cat_id)
            except:
                self.stdout.write(('Satellite {} with Identifier {} does '
                                  'not exist [deleted]').format(obj.name, obj.norad_cat_id))
                obj.delete()
                continue

            obj.name = sat.name()
            obj.save()
            self.stdout.write(('Satellite {} with Identifier {} '
                              'found [updated]').format(obj.norad_cat_id, obj.name))
