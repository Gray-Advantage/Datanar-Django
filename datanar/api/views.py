from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from redirects import models, serializers


class APIDocumentationView(TemplateView):
    template_name = 'api/api_docs.html'


class RedirectViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = models.Redirect.objects.all()
        serializer = serializers.RedirectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.Redirect.objects.all()
        redirect = get_object_or_404(queryset, pk=pk)
        serializer = serializers.RedirectSerializer(redirect)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = models.Redirect.objects.all()
        redirect = get_object_or_404(queryset, pk=pk)
        redirect.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        pass


__all__ = [RedirectViewSet]
