from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.contrib.auth.decorators import login_required

from .decorators import update_password
from django.contrib.auth import login
from .models import CustomUser, Teacher
from questions.models import Question


# Configurar a API do Google Gemini
genai.configure(api_key="AIzaSyAMBJfbMpW5iqt3XsqFjyIdhfFbfU7YbkE")
model = genai.GenerativeModel("gemini-pro")

@login_required(redirect_field_name='login')
@update_password
def chat_view(request):
    request.session['chat_history'] = []
    array_questions = Question.objects.all()
    return render(request, 'chatbot/chat.html', {'array_questions':array_questions})

def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print(message)
        response = generate_response(message, request)
        chat_history = request.session.get('chat_history', [])
        chat_history.append({'role': 'user', 'parts': [{'text': message}]},)
        chat_history.append({'role': 'model', 'parts': [{'text': response}]},)
        request.session['chat_history'] = chat_history
        return JsonResponse({'message': message, 'response': response})

def generate_response(message, request):
    chat_history = request.session.get('chat_history', [])

    # Iniciar o chat com o histórico existente
    chat = model.start_chat(history=chat_history)

    # Enviar a mensagem para o modelo
    response = chat.send_message(message)

    return response.candidates[0].content.parts[0].text



def update_password(request):

    if request.method == "POST":
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']

        if password == repeat_password:
            update_user = request.user
            update_user.set_password(password)
            update_user.reset_password = True
            update_user.save()
            login(request, update_user)
            return redirect('chat_view')
            
        else:
            return redirect('update_password')

    else:
        return render(request, 'chatbot/change_password.html')


@login_required(redirect_field_name='login')
def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'chatbot/list_users.html', {'users':users})


@login_required(redirect_field_name='login')
def list_teachers(request):
    teachers = Teacher.objects.all()
    
    for teacher in teachers:
        teacher.competency = teacher.competency.split(',')
    return render(request, 'chatbot/list_teachers.html', {'teachers':teachers})


def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    admin = request.POST['admin']
    password = request.POST['password']
    
    new_user = CustomUser.objects.create_user(username=username, email=email, password=password)
    
    if admin == '1':
        new_user.is_superuser = True
        new_user.save()

    
    return redirect('list-users')

def create_teacher(request):
    name = request.POST['name']
    education = request.POST['education']
    area = request.POST['area']
    competency = request.POST['competency']
    
    
    
    Teacher.objects.create(name=name, education=education, area=area, competency=competency)
    return redirect('list-teachers')
    
    
    