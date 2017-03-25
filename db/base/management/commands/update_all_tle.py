from orbit import satellite

from django.core.management.base import BaseCommand

from db.base.models import Satellite


class Command(BaseCommand):
    help = 'Update TLEs for existing Satellites'

    def handle(self, *args, **options):

        satellites = Satellite.objects.all()

        for obj in satellites:
            try:
                sat = satellite(obj.norad_cat_id)
            except:
                self.stdout.write(('Satellite {} with Identifier {} does '
                                  'not exist').format(obj.name, obj.norad_cat_id))
                continue

            obj.name = sat.name()
            tle = sat.tle()
            obj.tle1 = tle[1]
            obj.tle2 = tle[2]
            obj.save()
            self.stdout.write(('Satellite {} with Identifier {} '
                              'found [updated]').format(obj.name, obj.norad_cat_id))
