from django.urls import  path, re_path
from app import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index_view, name='home'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('dashboard', views.dashboard_view, name = "dashboard"),
    path('add_bin', views.AddBinsFormView.as_view(), name = "add_bin"),
    path('update/', views.UpdateBinsFormView.as_view(), name='update_bin'),
    path('details/', views.details_view, name='bin_details'),
    path('delete/', views.delete_view, name='delete_bin'),
    path('download/', views.download_view, name='download_bin'),
]