import logging

from django.core.management.base import BaseCommand
from django_sage_meta.repository.service import SyncService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Synchronize all data in the specified order: Categories, Users, Instagram Accounts, Facebook Pages, Media, Insights, Stories.'

    def show_success_msg(self, msg: str):
        """
        Display a success message on the console.

        Args:
        - msg (str): The success message.
        """
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error_msg(self, msg: str):
        """
        Display an error message on the console.

        Args:
        - msg (str): The error message.
        """
        self.stdout.write(self.style.ERROR(msg))

    def show_warning_msg(self, msg: str):
        """
        Display an error message on the console.

        Args:
        - msg (str): The error message.
        """
        self.stdout.write(self.style.WARNING(msg))

    def handle(self, *args, **kwargs):
        try:
            self.show_warning_msg('Starting synchronization...')

            self.show_warning_msg('Syncing Categories...')
            SyncService.sync_categories()
            self.show_success_msg('Categories synced successfully.')

            self.show_warning_msg('Syncing Users...')
            SyncService.sync_user_data()
            self.show_success_msg('Users synced successfully.')

            self.show_warning_msg('Syncing Instagram Accounts...')
            SyncService.sync_instagram_accounts()
            self.show_success_msg('Instagram Accounts synced successfully.')

            self.show_warning_msg('Syncing Facebook Pages...')
            SyncService.sync_facebook_pages()
            self.show_success_msg('Facebook Pages synced successfully.')

            self.show_warning_msg('Syncing Media...')
            SyncService.sync_media()
            self.show_success_msg('Media synced successfully.')

            self.show_warning_msg('Syncing Insights...')
            SyncService.sync_insights()
            self.show_success_msg('Insights synced successfully.')

            self.show_warning_msg('Syncing Stories...')
            SyncService.sync_stories()
            self.show_success_msg('Stories synced successfully.')

            self.show_success_msg('All data synchronized successfully.')

        except Exception as e:
            logger.error(f"An error occurred during synchronization: {e}")
            self.show_error_msg(f"An error occurred: {e}")
