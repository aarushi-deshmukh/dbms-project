from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('api')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        logger.error(
            'API exception: %s %s',
            exc.__class__.__name__,
            str(exc),
            exc_info=True
        )

        standardized = {
            'success': False,
            'message': getattr(exc, 'detail', 'An error occurred.'),
            'data': None,
            'error': {
                'type': exc.__class__.__name__,
                'detail': response.data,
            },
            'code': getattr(exc, 'default_code', 'error'),
        }
        return Response(standardized, status=response.status_code)

    logger.error('Unhandled exception: %s', str(exc), exc_info=True)
    return Response(
        {
            'success': False,
            'message': 'Internal server error',
            'data': None,
            'error': {'type': exc.__class__.__name__, 'detail': str(exc)},
            'code': 'server_error',
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
