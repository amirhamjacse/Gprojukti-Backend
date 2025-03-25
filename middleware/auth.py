import json
import logging
import jwt
from typing import Dict, List, Union

from django.http import HttpRequest, JsonResponse
from rest_framework.exceptions import ValidationError

from gporjukti_backend_v2.settings import SECRET_KEY
from user.models import UserAccount
from django.core.cache import cache

logger = logging.getLogger('django')


def get_cache(key: str) -> bool:
    try:
        return cache.get(key)
    except Exception as err:
        logger.info(f'cannot get cache data: {err}')
        return False

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_user(data: Dict) -> Union[UserAccount, object]:
        try:
            try:
                user_data = json.loads(get_cache(f'{data["username"]}_token_data'))
            except Exception:
                raise ValidationError(detail='user data not found', code=401)
            user = UserAccount.objects.get(username__exact=user_data['username'])
            if not user.is_active or not user.verified:
                return
            return user
        except UserAccount.DoesNotExist:
            return

    def __call__(self, request: HttpRequest):
        setattr(request, '_dont_enforce_csrf_checks', True)
        auth_header: str = request.headers.get('authorization')
        if auth_header:
            token_obj: List[str] = auth_header.split(' ')
            if token_obj[0].lower() != 'bearer':
                return JsonResponse(data={
                    'message': 'invalid token type',
                    'success': False,
                }, status=400)
            try:
                payload: Dict = jwt.decode(
                    jwt=token_obj[1], key=SECRET_KEY, algorithms='HS256', verify=True)
                if payload['token_type'] != 'access':
                    return JsonResponse(data={
                        'message': 'no access token provided',
                        'success': False
                    }, status=400)
                user_obj = self.get_user(data=payload)
                if not user_obj:
                    return JsonResponse(data={
                        'message': 'cannot retrieve user information',
                        'success': False
                    }, status=401)
                setattr(request, 'user', user_obj)
            except Exception as err:
                return JsonResponse(data={
                    'message': f'{str(err)}',
                    'success': False,

                    
                }, status=401)
        response = self.get_response(request)
        return response
