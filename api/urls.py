from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
     path('users', views.UserListView.as_view(), name='users'),
    path('test/', views.testEndPoint, name='test'),
    path('token_crsf', views.get_csrf_token, name='token'),
    path('', views.getRoutes),

    # Todo URLS
    path("todo/<user_id>/", views.TodoListView.as_view()),
    path("todos/<user_id>", views.TodoListView.as_view()),
    path("todo-detail/<user_id>/<todo_id>/", views.TodoDetailView.as_view()),
    path("todo-mark-as-completed/<user_id>/<todo_id>/", views.TodoMarkAsCompleted.as_view()),
    path('todo-update/<int:user_id>/<int:todo_id>/', views.TodoUpdateView.as_view(), name='todo-update'), 
]