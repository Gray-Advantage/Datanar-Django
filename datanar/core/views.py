__all__ = ("csrf_failure", "server_error")

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import defaults
from django.views.decorators.csrf import requires_csrf_token

logger = logging.getLogger(__name__)


@requires_csrf_token
def csrf_failure(
    request: HttpRequest,
    reason: str = "",
    template_name: str = "403_csrf.html",
) -> HttpResponse:
    return render(request, template_name, status=403)


@requires_csrf_token
def server_error(
    request: HttpRequest,
    template_name: str = "500.html",
) -> HttpResponse:
    try:
        return render(request, template_name, status=500)
    except Exception:
        logger.exception("Rendering %s with a request failed", template_name)
        return defaults.server_error(request, template_name)
