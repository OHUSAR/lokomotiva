from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class SendMail(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            'Subject here',
            'Here is the message.',
            'noreply@skilokomotiva.sk',
            ['ondrej@husar.sk'],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Sent mail.'))
