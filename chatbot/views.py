import json
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse, JsonResponse
import google.generativeai as genai
from django.contrib.auth.decorators import login_required


from .decorators import update_password
from django.contrib.auth import login
from .models import CustomUser, Teacher, Briefing
from questions.models import Question

from django.views.decorators.csrf import csrf_exempt
from chatbot.services import generate_doc



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
    users = CustomUser.objects.all().order_by('-id')
    return render(request, 'chatbot/list_users.html', {'users':users})


@login_required(redirect_field_name='login')
def list_teachers(request):
    teachers = Teacher.objects.all().order_by('-id')
    
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
    
    
    
@csrf_exempt
def download_doc(request):
    if request.method == "POST":
        proposal = request.POST.get('proposal')
        proposal_json = json.loads(proposal)
        file = generate_doc(proposal_json)
    
        response = FileResponse(file, as_attachment=True, filename="generated.docx")
        
        response['File-Path'] = file.name
        
        return response

    return HttpResponse(status=405) 
    
    


def list_proposals(request):
    proposals = Briefing.objects.all().order_by('-id')
    return render(request, 'chatbot/list_proposals.html', {'proposals':proposals})



def update_proposal(request):

    id = request.POST.get('id')
    question_16 = request.POST.get('question_16')
    question_17 = request.POST.get('question_17')
    question_18 = request.POST.get('question_18')
    question_19 = request.POST.get('question_19')
    question_20 = request.POST.get('question_20')
    question_21 = request.POST.get('question_21')
    question_22 = request.POST.get('question_22')
    question_23 = request.POST.get('question_23')
    question_24 = request.POST.get('question_24')



    proposal = Briefing.objects.get(id=id)
    proposal.question_16 = question_16
    proposal.question_17 = question_17
    proposal.question_18 = question_18
    proposal.question_19 = question_19
    proposal.question_20 = question_20
    proposal.question_21 = question_21
    proposal.question_22 = question_22
    proposal.question_23 = question_23
    proposal.question_24 = question_24
    proposal.completed = True
    proposal.save()
    print(question_24)
    return HttpResponse("Proposta atualizada.")



def form_briefing(request):

    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        question_1 = request.POST.get('question_1')
        question_2 = request.POST.get('question_2')
        question_3 = request.POST.get('question_3')
        question_4 = request.POST.get('question_4')
        question_5 = request.POST.get('question_5')
        question_6 = request.POST.get('question_6')
        question_7 = request.POST.get('question_7')
        question_8 = request.POST.get('question_8')
        question_9 = request.POST.get('question_9')
        question_10 = request.POST.get('question_10')
        question_11 = request.POST.get('question_11')
        question_12 = request.POST.get('question_12')
        question_13 = request.POST.get('question_13')
        question_14 = request.POST.get('question_14')
        question_15 = request.POST.get('question_15')

        Briefing.objects.create(
            phone=phone,
            email=email,
            question_1=question_1,
            question_2=question_2,
            question_3=question_3,
            question_4=question_4,
            question_5=question_5,
            question_6=question_6,
            question_7=question_7,
            question_8=question_8,
            question_9=question_9,
            question_10=question_10,
            question_11=question_11,
            question_12=question_12,
            question_13=question_13,
            question_14=question_14,
            question_15=question_15
        )

        return redirect('briefing')
        


    else:
        return render(request, 'chatbot/briefing.html')    
