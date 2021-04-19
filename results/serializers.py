from rest_framework import serializers

from .models import AllureResult


class AllureResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllureResult
        fields = ('id', 'results', 'uploaded_at')

