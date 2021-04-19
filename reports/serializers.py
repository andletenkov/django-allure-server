from rest_framework import serializers

from .models import AllureReport


class AllureReportBaseSerializer(serializers.ModelSerializer):
    path = serializers.ListField(allow_empty=False)

    class Meta:
        model = AllureReport


class AllureReportGetSerializer(AllureReportBaseSerializer):
    class Meta(AllureReportBaseSerializer.Meta):
        fields = ('id', 'path', 'url', 'created_at')


class AllureReportCreateSerializer(AllureReportBaseSerializer):
    results_id = serializers.IntegerField(min_value=1)

    class Meta(AllureReportBaseSerializer.Meta):
        fields = ('id', 'results_id', 'path')
