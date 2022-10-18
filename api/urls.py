import django


from django.urls import path
from . import views

urlpatterns = [
    path('get_garbage_data/', views.get_garbage_data, name='get_garbage_data'),
    path('add_garbage_data/', views.add_garbage_data, name='add_garbage_data'),
]
