from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AllureReport
from .serializers import AllureReportGetSerializer, AllureReportCreateSerializer


class AllureReportListView(APIView):

    def get(self, request):
        reports = AllureReport.objects.all()
        serialized = AllureReportGetSerializer(reports, many=True)
        return Response(serialized.data)

    def post(self, request):
        serialized = AllureReportCreateSerializer(data=request.data)
        if serialized.is_valid():
            report = AllureReport.generate(**serialized.data)
            url = f'{request.scheme}://{request.get_host()}{report.url}'
            return Response({
                'url': url
            })
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class AllureReportDetailView(APIView):
    serializer = AllureReportGetSerializer

    def get(self, request, id):
        report = get_object_or_404(AllureReport, pk=id)
        serialized = self.serializer(report)
        return Response(serialized.data)

    def delete(self, request, id):
        report = get_object_or_404(AllureReport, pk=id)
        serialized = self.serializer(report)
        report_id = serialized.data['id']
        report.delete()
        return Response({
            'id': report_id
        })
