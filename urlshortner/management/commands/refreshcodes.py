from django.core.management.base import BaseCommand, CommandError
from urlshortner.models import weeURL

class Command(BaseCommand):
    help = 'Refreshes All weeURL shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
    	# print(options) 
    	return weeURL.objects.refresh_shortcodes(items=options['items'])