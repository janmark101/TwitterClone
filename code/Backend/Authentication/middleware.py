# middleware.py
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialAccount

class GmailAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(request.user,'z middleware')
        if request.path in ['/accounts/google/login/','/accounts/logout/']:
            print('google')
            print(request.user,'z google')
            # if not Token.objects.filter(user=request.user).exists():
            #     Token.objects.create(user=request.user)
            # else: 
            #     Token.objects.filter(user=request.user).delete()
        return response

# class CustomAuthenticationMiddleware:
    
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # # Sprawdź, czy żądanie dotyczy logowania lub rejestracji
#         # is_login_request = request.path.startswith(self.LOGIN_ENDPOINT_PREFIX)
#         # #is_register_request = request.path.startswith(self.REGISTER_ENDPOINT_PREFIX)

#         # if not (is_login_request ): #or is_register_request
#         #     # Sprawdź, czy użytkownik jest zalogowany, tylko jeśli nie jest to logowanie ani rejestracja
#         #     if not request.user.is_authenticated:
#         #         # Użytkownik jest zalogowany, kontynuuj przetwarzanie żądania
#         #         return Response({"detail": "Użytkownik niezalogowany."}, status=status.HTTP_401_UNAUTHORIZED)

#         # # Jeśli to jest logowanie lub rejestracja lub użytkownik nie jest zalogowany, przejdź dalej
#         # return self.get_response(request)
#         ADMIN_ENDPOINT_PREFIX = '/admin/'
#         LOGIN_ENDPOINT_PREFIX = '/auth/login/'
#         REGISTER_ENDPOINT_PREFIX = '/auth/register/'

#         print(request.path)
#         if request.path in []:
#             auth_token = request.META.get('HTTP_AUTHORIZATION')
#             if auth_token == None: 
#                 return JsonResponse({'error': 'You dont have permission'})
        
#         return self.get_response(request) 