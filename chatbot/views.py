from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from questions import services as QuestionService

# Configurar a API do Google Gemini
genai.configure(api_key="AIzaSyAMBJfbMpW5iqt3XsqFjyIdhfFbfU7YbkE")
model = genai.GenerativeModel("gemini-pro")

@login_required(redirect_field_name='login')
def chat_view(request):
    request.session['chat_history'] = [{"parts":[{"text":"Olá"}]}]
    return render(request, 'chatbot/chat.html')

def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        request.session['chat_history'] = [{"parts":[{"text":"Olá"}]}]
        return JsonResponse({'message': message, 'response': "Olá"})
        # Traz todas as perguntas colocadas no banco
        QuestionService.get_ordered_questions()
    
        # Ajustar para realizar as perguntas antes de começar com o Gemini
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





@login_required(redirect_field_name='login')
def list_users(request):
    users = User.objects.all()
    return render(request, 'chatbot/list_users.html', {'users':users})


def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    admin = request.POST['admin']
    password = request.POST['password']
    
    new_user = User.objects.create_user(username=username, email=email, password=password)
    
    if admin == '1':
        new_user.is_superuser = True
        new_user.save()

    
    return redirect('list-users')
    
    
    