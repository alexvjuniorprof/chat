from django.urls import path, include
from chatbot import views
from django.contrib import admin

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('admin/', admin.site.urls),
    path('send_message/', views.send_message, name='send_message'),
    path('accounts/', include('accounts.urls')),
    path('list-users/', views.list_users, name='list-users'),
    path('create-user/', views.create_user, name='create-user'),
    path('change-password/', views.update_password, name='change_password'),

]
