from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Initialize database for production deployment'
    
    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(
                self.style.SUCCESS('Superuser "admin" created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            )