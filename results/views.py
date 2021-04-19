from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AllureResult
from .serializers import AllureResultSerializer


class AllureResultListView(APIView):
    serializer = AllureResultSerializer

    def get(self, request):
        results = AllureResult.objects.all()
        serialized = self.serializer(results, many=True)
        return Response(serialized.data)

    def post(self, request):
        serialized = self.serializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            results_id = serialized.data['id']
            return Response({
                'id': results_id
            })
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class AllureResultDetailView(APIView):
    serializer = AllureResultSerializer

    def get(self, request, id):
        results = get_object_or_404(AllureResult, pk=id)
        serialized = self.serializer(results)
        return Response(serialized.data)

    def delete(self, request, id):
        results = get_object_or_404(AllureResult, pk=id)
        serialized = self.serializer(results)
        results_id = serialized.data['id']
        results.delete()
        return Response({
            'id': results_id
        })