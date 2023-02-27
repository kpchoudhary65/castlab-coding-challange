from django.db.models import Q
from django.http import HttpRequest
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from .models import License, Package, LicenseType
from .notifications import EmailNotification
from django.core import mail
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import MailSerializer


class SendMailView(APIView):
    email_template = 'email.html'
    email_notification = EmailNotification()

    def get(self, request: HttpRequest) -> Response:
        mails = mail.outbox
        serializer = MailSerializer(mails, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        four_month_condition = Q(expiration_datetime__range=[datetime.now(), datetime.now() + relativedelta(months=4)])
        monday_condition = Q(
            expiration_datetime=(datetime.now() + relativedelta(months=1))) if date.today().weekday() == 0 else Q()
        week_condition = Q(expiration_datetime__range=[datetime.now(), datetime.now() + relativedelta(months=4)])

        licenses = License.objects.filter(four_month_condition | monday_condition | week_condition).all()
        for license in licenses:
            context = {
                "license": license,
                "license_type": next((type.name for type in LicenseType if type.value == license.license_type), None),
                "package_name": next((package.name for package in Package if package.value == license.license_type),
                                     None)
            }
            self.email_notification.template_path = self.email_template
            self.email_notification.send_notification([license.client.poc_contact_email], context)
        return Response({"message": "Mail Sent Successfully"})
