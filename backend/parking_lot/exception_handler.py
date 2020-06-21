from django.utils.translation import ugettext as _

from rest_framework.views import exception_handler


def create_exception_object(detail, fields):
    return {
        'errors': {
            'message': detail,
            'fields': fields
        }
    }


def get_custom_exception_object(data):
    if 'detail' in data:
        data = create_exception_object(data['detail'], None)
    elif isinstance(data, dict):
        data = create_exception_object(_('Invalid payload'), data)

    return data


def parking_lot_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = get_custom_exception_object(response.data)

    return response
