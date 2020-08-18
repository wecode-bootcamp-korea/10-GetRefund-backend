import jwt, json


from django.http    import JsonResponse
from my_settings    import SECRET_KEY, ALGORITHM
from .models        import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            data         = jwt.decode(access_token, SECRET_KEY['secret'], ALGORITHM['algorithm'])
            user         = User.objects.get(id=data['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse ({'message': 'INVALID_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse ({'message': 'INVALID_USER'}, status=400)
        except KeyError:
            return JsonResponse ({'message': 'KEY_ERROR'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper


