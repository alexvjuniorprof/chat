from django.urls import path, include
from chatbot import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send_message/', views.send_message, name='send_message'),
    path("accounts/", include("accounts.urls"))
]
