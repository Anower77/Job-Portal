from django.core.management.base import BaseCommand
from account.models import CustomUser

class Command(BaseCommand):
    help = 'Creates a custom superuser with all required fields'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--first_name', default='Super')
        parser.add_argument('--last_name', default='Admin')

    def handle(self, *args, **options):
        try:
            user = CustomUser.objects.create_superuser(
                email=options['email'],
                password=options['password'],
                first_name=options['first_name'],
                last_name=options['last_name']
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {user.email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}')) 