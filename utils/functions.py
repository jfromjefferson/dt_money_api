from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

from api_v1.models import SysUser, Owner


def get_owner(request: WSGIRequest) -> [bool, Owner]:
    success = True

    try:
        sys_user = get_object_or_404(SysUser, uuid=request.headers.get('Sys-user-uuid'))

        return success, sys_user.owner
    except Exception as error:
        success = False

        message_dict = {
            'message': 'Missing sys-user authentication',
            'exception': str(error),
            'status_code': 400
        }

        return success, message_dict


def get_error_dict(serializer: ModelSerializer, status_code: int):
    error_dict = {}

    for key, value in serializer.errors.items():
        error_dict[key] = value[0]

    return JsonResponse(error_dict, status=status_code if status_code else 200)


def response_message(message_dict: dict):
    response = JsonResponse(message_dict)

    response.status_code = message_dict.get('status_code')

    return response
