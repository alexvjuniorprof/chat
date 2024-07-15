from django.shortcuts import render, redirect
from django.contrib import auth



def login(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        authenticate = auth.authenticate(request, username=username, password=password)
        
        if authenticate:
            auth.login(request, authenticate)
            return redirect("chat_view")

        else:
            return redirect("login")
        
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout()
    return redirect("login")


