from django.urls import path
from .views import menu_view

urlpatterns = [
    path('', menu_view, name='page'),
    path('<path:name>/', menu_view, name='page'),
]
