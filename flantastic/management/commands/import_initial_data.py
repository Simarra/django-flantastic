from django.core.management.base import BaseCommand
from flantastic.data.bakeries_downloader import download_bakeries
from flantastic.data.bakeries_importer import import_bakeries
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, **options):
        # now do the things that you want with your models here
        logger.info("downloading bakeries")
        download_bakeries()

        logger.info("Importing bakeries to database.")
        import_bakeries()

        logger.info(" SUCCESSFULLY GEOSIRENE IMPORTED INTO DB!")