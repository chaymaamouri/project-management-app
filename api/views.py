from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from api.models import User, Todo

from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer, TodoSerializer, UserSerializer

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


class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        todo = Todo.objects.filter(user=user) 
        return todo
 

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