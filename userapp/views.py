from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views import View
import json
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny

# Create your views here.

class Adminhomeload(View):
    def get(self, request):
        return render(request, 'user/adminhome.html')    


    
class UserLogin(View):
    template_name = "user/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        response_dict = {"success": False}
        landing_page_url = {
            "ADMIN": "userapp:loadadmin",
            "TURF": "turfapp:loadturf",
           
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        authenticated = authenticate(username=username, password=password)
        
        try:
            user = Userprofile.objects.get(username=username)
        except Userprofile.DoesNotExist:
            response_dict["reason"] = "No account found for this username. Please signup."
            messages.error(request, response_dict["reason"])
            return redirect("userapp:userlogin")

        if not authenticated:
            response_dict["reason"] = "Invalid credentials."
            messages.error(request, response_dict["reason"])
            return redirect("userapp:userlogin")
        
        session_dict = {"real_user": authenticated.id}
        token, _ = Token.objects.get_or_create(
            user=user, defaults={"session_dict": json.dumps(session_dict)}
        )

        user_type = authenticated.user_type

        request.session["data"] = {
            "user_id": user.id,
            "user_type": user.user_type,
            "token": token.key,
            "username": user.username,
            "status": user.is_active,
        }
        request.session["user_id"]=user.id
        request.session["user"] = authenticated.username
        request.session["token"] = token.key
        request.session["status"] = user.is_active
        return redirect(landing_page_url.get(user_type, "userapp:userlogin"))
    


class UserLoginapi(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = tuple()

    def get(self, request):
        response_dict = {"status": False}
        response_dict["logged_in"] = bool(request.user.is_authenticated)
        response_dict["status"] = True
        return Response(response_dict, HTTP_200_OK)

    def post(self, request):
        response_dict = {"status": False, "token": None, "redirect": False}
        password = request.data.get("password")
        username = request.data.get("username")
        try:
            t_user = Userprofile.objects.get(username=username)
        except Userprofile.DoesNotExist:
            response_dict["reason"] = "No account found for this username. Please signup."
            return Response(response_dict, HTTP_200_OK)

        # today = utc_today()
        authenticated = authenticate(username=t_user.username, password=password)
        if not authenticated:
            response_dict["reason"] = "Invalid credentials."
            return Response(response_dict, HTTP_200_OK)

        user = t_user
        if not user.is_active:
            response_dict["reason"] = "Your login is inactive! Please contact admin"
            return Response(response_dict, HTTP_200_OK)

        session_dict = {"real_user": authenticated.id}
        token, c = Token.objects.get_or_create(
            user=user, defaults={"session_dict": json.dumps(session_dict)}
        )
        login(request, user, "django.contrib.auth.backends.ModelBackend")
        response_dict["session_data"] = {
            "user_id": user.id,
            "user_type": user.user_type,
            "token": token.key,
            "username": user.username,
            "name": user.first_name,
            "status": user.status,
        }
        response_dict["token"] = token.key
        response_dict["status"] = True
        return Response(response_dict,HTTP_200_OK)
