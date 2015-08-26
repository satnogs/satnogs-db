from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Create initial fixtures'

    def handle(self, *args, **options):
        # Migrate
        call_command('migrate')

        #  Initial data
        call_command('loaddata', 'modes')
        call_command('loaddata', 'satellites')
        call_command('loaddata', 'transmitters')

        # Create superuser
        call_command('createsuperuser')
