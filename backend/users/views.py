from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import QuizProgress, CustomUser, JobApplication
import json
from .models import CustomUser, QuizProgress, JobApplication, LearningProgress


User = get_user_model()

@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name', '')

    if User.objects.filter(email=email).exists():
        return Response({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password, name=name)
    return Response({'message': 'User registered successfully'})

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    if user is not None:
        serializer = UserSerializer(user)
        return Response({'message': 'Login successful', 'user': serializer.data})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def submit_quiz_score(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        score = data.get("score")
        quiz_title = data.get("quiz_title")

        try:
            user = CustomUser.objects.get(id=user_id)
            QuizProgress.objects.create(user=user, score=score, quiz_title=quiz_title)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import QuizProgress, CustomUser  # or use get_user_model
import json

@csrf_exempt
def get_quiz_history(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")

            progress = QuizProgress.objects.filter(user_id=user_id).order_by('-timestamp')

            history = [{
                "quiz_title": q.quiz_title,
                "score": q.score,
                "timestamp": q.timestamp.strftime("%Y-%m-%d %H:%M")
            } for q in progress]

            return JsonResponse({"success": True, "data": history})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def apply_job(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = CustomUser.objects.get(id=data["user_id"])
            JobApplication.objects.create(
                user=user,
                company=data["company"],
                role=data["role"]
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def save_learning_progress(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            topic = data.get("topic")

            user = CustomUser.objects.get(id=user_id)
            LearningProgress.objects.create(user=user, topic=topic)

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
