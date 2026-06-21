from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create the default eden admin account'

    def handle(self, *args, **options):
        if not User.objects.filter(username='eden').exists():
            User.objects.create_superuser(
                username='eden',
                email='admin@ebooks.local',
                password='eden123',
            )
            self.stdout.write(self.style.SUCCESS('Created admin user: eden / eden123'))
        else:
            self.stdout.write('Admin user eden already exists')
