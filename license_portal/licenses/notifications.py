from typing import List, Any
from django.template import Template
from django.template.loader import get_template
from django.conf import settings
from django.core import mail

email_backend = 'django.core.mail.backends.locmem.EmailBackend'
connection = mail.get_connection(backend=email_backend)


class EmailNotification:
    """ A convenience class to send email notifications
    """
    subject = "Your License for [Product Name] is Expiring Soon"
    from_email = settings.EMAIL_HOST_USER
    template_path = "email.html"

    @classmethod
    def load_template(cls) -> Template:
        """Load the configured template path"""
        return get_template(cls.template_path)

    @classmethod
    def send_notification(cls, recipients: List[str], context: Any) -> None:
        """Send the notification using the given context"""
        template = cls.load_template()
        message_body = template.render(context=context)
        email = mail.EmailMessage(
            subject=cls.subject,
            from_email=cls.from_email,
            to=recipients,
            body=message_body,
            connection=connection
        )
        email.send()

