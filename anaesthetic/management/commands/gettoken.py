from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create REST Token Auth key'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
            u = User.objects.get(username=options['username'])
            try:
                token = Token.objects.create(user=u)
            except:
                token = Token.objects.get(user=u)

            self.stdout.write('Token: %s' % token.key)