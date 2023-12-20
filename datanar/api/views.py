import hashlib

from django.views.generic import TemplateView
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from sqids import Sqids

from redirects import models, serializers
from users import models as user_models


sqids = Sqids()


class APIDocumentationView(TemplateView):
    template_name = "api/api_docs.html"


class RedirectViewSet(viewsets.ViewSet, mixins.CreateModelMixin):
    def get_user(self, request):
        if request.query_params.get("token"):
            token = request.query_params.get("token")
        else:
            token = request.data.get("token")
        token_instance = Token.objects.filter(key=token).first()
        user = token_instance.user if token_instance else None
        if request.user.is_authenticated and not user:
            return request.user
        return user

    def list(self, request):
        user = self.get_user(request)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = models.Redirect.objects.filter(user=user)
        serializer = serializers.RedirectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.get_user(request)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = models.Redirect.objects.all()
        redirect = get_object_or_404(queryset, pk=pk, user=user)
        serializer = serializers.RedirectSerializer(redirect)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = self.get_user(request)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = models.Redirect.objects.filter(user=user)
        redirect = get_object_or_404(queryset, pk=pk, user=user)
        redirect.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):  # noqa: CFQ004
        if request.data.get("long_link") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer_data = {}

        short_link = request.data.get("short_link")

        if short_link and (
            "/" in short_link
            or models.Redirect.objects.get_by_short_link(short_link)
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not short_link:
            counter = 0
            string = request.data.get("long_link")
            while True:
                temp_string = f"{string}{counter}" if counter > 0 else string
                hash_object = hashlib.sha256(temp_string.encode())
                number = int.from_bytes(hash_object.digest(), byteorder="big")
                short_link = sqids.encode(list(map(int, list(str(number)))))[
                    :5
                ]
                if not models.Redirect.objects.get_by_short_link(short_link):
                    break
                counter += 1

        user = self.get_user(request)
        if user:
            serializer_data.update({"user": user})

        if (
            "validity_days" in request.data
            or "validity_clicks" in request.data
            or "password" in request.data
        ) and not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer_data.update({"short_link": short_link})
        serializer = serializers.RedirectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**serializer_data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


__all__ = [RedirectViewSet]
