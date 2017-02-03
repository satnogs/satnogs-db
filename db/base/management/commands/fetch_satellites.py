from orbit import satellite

from django.core.management.base import BaseCommand, CommandError

from db.base.models import Satellite


class Command(BaseCommand):
    help = 'Updates/Inserts Name for certain Satellites'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('satellite_identifiers',
                            nargs='+',
                            metavar='<Satellite Identifier>')

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete Satellite'
        )

    def handle(self, *args, **options):
        for item in options['satellite_identifiers']:
            if options['delete']:
                try:
                    Satellite.objects.get(norad_cat_id=item).delete()
                    self.stdout.write('Satellite {}: deleted'.format(item))
                    continue
                except:
                    raise CommandError('Satellite with Identifier {} does not exist'.format(item))

            try:
                sat = satellite(item)
            except:
                raise CommandError('Satellite with Identifier {} does not exist'.format(item))

            try:
                obj = Satellite.objects.get(norad_cat_id=item)
            except:
                obj = Satellite(norad_cat_id=item)

            obj.name = sat.name()
            obj.save()

            self.stdout.write('fetched data for {}: {}'.format(obj.norad_cat_id, obj.name))
