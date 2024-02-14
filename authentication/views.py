from django.http import JsonResponse
from rest_framework import generics ,status ,views
from rest_framework.request import Request
from rest_framework.response import Response
from . import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,DjangoUnicodeDecodeError,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from django.urls import reverse



class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer
    
    def post(self,request:Request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        
        user=User.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user).access_token
        current_site=get_current_site(request).domain
        relativeLink=reverse('email-verify')
        absurl='http://'+current_site+relativeLink+"?token"+str(token)
        email_body= 'Hi '+ user.username + 'use link below to verify your account\n'+absurl
        data={
            'email_body':email_body,
            'email_subject': 'verify your email',
            'to_email': user.email
        }
        Util.send_email(data)
        
        
        return Response(user_data,status=status.HTTP_200_OK)
    


class VerifyEmail(views.APIView):
    serializer_class = serializers.EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return JsonResponse({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id is None:
                return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(id=user_id)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'message': 'Email successfully activated'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the exception for further investigation
            print(f"Exception: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LoginView(generics.GenericAPIView):
    serializer_class=serializers.LoginSerializer
    
    def post(self,request:Request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        response=serializer.data
        return Response(data=response,status=status.HTTP_200_OK)
    

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = serializers.RequestPasswordResetEmailSerializer
    
    def post(self,request:Request):
        serilizer=self.serializer_class(data=request.data)
        email=request.data['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(request=request).domain
            relativeLink=reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            absurl='http://'+current_site+relativeLink
            email_body= 'Hellow '+ user.username + ' use link below to reset your password\n'+absurl
            data={
                'email_body':email_body,
                'email_subject': 'reset your password',
                'to_email': user.email
                }
            Util.send_email(data)
        return Response({'success':'we have sent you a link to reset your password'},status=status.HTTP_200_OK)
    
    
    
class PasswordTokenCheckApi(generics.GenericAPIView):
   
   
   
   def get(self,request,uidb64,token):
       
       try:
           id=smart_str(urlsafe_base64_decode(uidb64))
           user=User.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user,token=token):
               return Response({'error':'token is not valid anymore request new one'},status=status.HTTP_401_UNAUTHORIZED)
           return Response({'sucess':True,'message':'credetials valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
           
           
           
           
       except DjangoUnicodeDecodeError as e:
            if not PasswordResetTokenGenerator().check_token(user,token=token):
               return Response({'error':'token is not valid anymore request new one'},status=status.HTTP_401_UNAUTHORIZED)
           

class SetNewPassword(generics.GenericAPIView):
    serializer_class=serializers.SetNewPasswordSerializer
    
    
    def patch(self,request:Request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'password reset success'},status=status.HTTP_200_OK)
    
           
        