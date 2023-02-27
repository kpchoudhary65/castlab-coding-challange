from rest_framework import serializers


class MailSerializer(serializers.Serializer):
    to = serializers.ListField(child=serializers.CharField())
    subject = serializers.CharField()
    body = serializers.CharField()
    from_email = serializers.CharField()
