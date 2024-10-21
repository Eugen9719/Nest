import os
from django.core.management.base import BaseCommand


from user import models

User = models.User


class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        username = os.getenv('SUPERUSER_NAME', 'admin')
        password = os.getenv('SUPERUSER_PASSWORD', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
