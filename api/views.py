import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from api.models import Project, Team, User, Todo

from api.serializer import MyTokenObtainPairSerializer, ProjectSerializer, RegisterSerializer, TeamSerializer, TodoSerializer, UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from rest_framework.generics import ListCreateAPIView
from api.serializer import ProjectSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_csrf_token(request):
    return JsonResponse({'csrf_token': get_token(request)})

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
        'api/token_crsf'
        
        
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


from datetime import datetime

from datetime import datetime

from datetime import datetime

class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        todos = Todo.objects.filter(user=user) 
        
        # Formater la date pour chaque objet Todo
        for todo in todos:
            if isinstance(todo.deadline, str):  # Vérifiez si la date est une chaîne
                todo.deadline = self.format_date(todo.deadline)
        
        return todos

    def format_date(self, date_string):
        try:
            # Convertir la chaîne de date en objet datetime
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
            return date_object
        except ValueError:
            # Gérer les erreurs de format de date invalide
            print("Format de date invalide")
            return None

    
@api_view(['PUT'])
def update_todo(request, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

class TodoUpdateView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']  # Utilisez 'id' au lieu de 'user_id'
        todo_id = self.kwargs['todo_id']

        user = get_object_or_404(User, id=user_id)
        todo = get_object_or_404(Todo, id=todo_id, user=user)

        return todo
  

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)

        return todo
    

class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)

        todo.completed = True
        todo.save()

        return todo
    
@api_view(['GET'])
def search_todos(request):
    if 'date' in request.query_params:
        # Recherche par date
        date = request.query_params.get('date')
        todos = Todo.objects.filter(date=date)
    elif 'title' in request.query_params:
        # Recherche par titre
        title = request.query_params.get('title')
        todos = Todo.objects.filter(title__icontains=title)
    else:
        # Aucun paramètre de recherche fourni
        return Response({"error": "Provide 'date' or 'title' parameter for search."}, status=400)

    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)
    
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_project(request):
    if request.method == 'POST':
        # Décoder les données JSON du corps de la requête en un dictionnaire Python
        request_data = json.loads(request.body)

        # Définir l'utilisateur connecté comme propriétaire du projet
        request_data['owner'] = request.user.id
        
        serializer = ProjectSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        # Récupérer tous les projets de l'utilisateur connecté
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

  


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def create_team(request):
    if request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        teams = Team.objects.filter(owner=request.user)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)