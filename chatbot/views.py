from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

# Configurar a API do Google Gemini
genai.configure(api_key="AIzaSyAMBJfbMpW5iqt3XsqFjyIdhfFbfU7YbkE")
model = genai.GenerativeModel("gemini-pro")

def chat_view(request):
    request.session['chat_history'] = []
    return render(request, 'chatbot/chat.html')

def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
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
