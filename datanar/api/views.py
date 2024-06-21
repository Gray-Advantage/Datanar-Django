from functools import wraps

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from redirects.forms import RedirectFormExtended
from redirects.models import Redirect
from redirects.serializers import RedirectCreateSerializer, RedirectSerializer


def authorization_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        user = self._get_user(request)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return view_func(self, request, user, *args, **kwargs)

    return _wrapped_view


class APIDocumentationView(TemplateView):
    template_name = "api/api_docs.html"


class DefaultWrongView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RedirectViewSet(viewsets.ViewSet, mixins.CreateModelMixin):
    def _get_user(self, request):
        token = request.query_params.get("token", request.data.get("token"))
        token_instance = Token.objects.filter(key=token).first()
        user = token_instance.user if token_instance else None
        if request.user.is_authenticated and not user:
            return request.user
        return user

    @authorization_required
    def list(self, request, user):
        serializer = RedirectSerializer(
            Redirect.objects.filter(user=user),
            many=True,
        )
        return Response(serializer.data)

    @authorization_required
    def retrieve(self, request, user, pk=None):
        if not pk.isdigit() or int(pk) <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = RedirectSerializer(
            get_object_or_404(Redirect, pk=pk, user=user),
        )
        return Response(serializer.data)

    @authorization_required
    def destroy(self, request, user, pk=None):
        if not pk.isdigit() or int(pk) <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        get_object_or_404(Redirect, pk=pk, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        if set(request.data) & {
            "validity_days",
            "validity_clicks",
            "password",
        }:
            if not self._get_user(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        post_data = request.data.copy()
        if "short_link" in post_data:
            post_data["custom_url"] = post_data.get("short_link")
            del post_data["short_link"]

        form = RedirectFormExtended(post_data)
        if form.is_valid():
            serializer = RedirectCreateSerializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(**{"short_link": form.cleaned_data["short_link"]})

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data),
            )
        responses = {
            (
                "long_link",
                _("This field is required."),
            ): status.HTTP_400_BAD_REQUEST,
            (
                "long_link",
                _("Enter a valid URL."),
            ): status.HTTP_400_BAD_REQUEST,
            (
                "long_link",
                _("this_url_is_blocked"),
            ): status.HTTP_423_LOCKED,
            (
                "custom_url",
                _("custom_url_already_use"),
            ): status.HTTP_409_CONFLICT,
        }
        for key, value in form.errors.items():
            if (key, *value) in responses:
                return Response(status=responses[(key, *value)])
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateNewTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({"token": token.key})


__all__ = [RedirectViewSet, CreateNewTokenView]
