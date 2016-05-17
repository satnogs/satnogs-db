from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Create initial fixtures'

    def handle(self, *args, **options):
        # Migrate
        self.stdout.write("Creating database...")
        call_command('migrate')

        #  Initial data
        self.stdout.write("Creating fixtures...")
        call_command('loaddata', 'modes')
        call_command('loaddata', 'satellites')
        call_command('loaddata', 'transmitters')

        # Create superuser
        self.stdout.write("Creating a superuser...")
        call_command('createsuperuser')
