from http import HTTPStatus

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flag


HEADERS_X_LIGHTS_UPDATED_AT = "x-lights-updated-at"

class FlagAPIView(APIView):
    def get(self, request, name):
        try:
            flag = Flag.objects.get(name=name)
        except Flag.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)

        headers = {
            HEADERS_X_LIGHTS_UPDATED_AT: flag.updated_at.microsecond
        }

        if flag.is_enabled:
            return Response(status=HTTPStatus.OK, headers=headers)
        return Response(status=HTTPStatus.NO_CONTENT, headers=headers)