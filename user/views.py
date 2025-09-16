from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


class UserViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserRegistrationApiView(APIView):
    permission_classes =[AllowAny]
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"http://127.0.0.1:8000/api/user/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    permission_classes =[AllowAny]
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

class UserLoginApiView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
        


class ContactUsAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.ContactUsSerializer
    
    def post(self, request, *args, **kwargs):
        user = request.user
        message = request.data.get('message')

        if not message:
            return Response({'error': 'Message field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        contact_data = {
            'name': user.username,
            'email': user.email,
            'message': message
        }

        serializer = self.serializer_class(data=contact_data)

        if serializer.is_valid():
            serializer.save()
            try:
                self.send_email(contact_data)
                return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Saved but failed to send email.', 'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, contact_data):
        subject = 'Received Contact Message'
        message = f"""
        Hello,

        You have received a new contact message.

        Details:
        Name: {contact_data.get('name')}
        Email: {contact_data.get('email')}
        Message: {contact_data.get('message')}

        """

        recipient_email = settings.EMAIL_HOST_USER

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False,
        )

