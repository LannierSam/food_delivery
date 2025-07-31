from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
]