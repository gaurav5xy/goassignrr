from django.urls import path
from . import views

app_name = 'assignment'

urlpatterns = [
    path('google5c48ed90c9c2a47a.html/', views.GoogleSearchConsoleView.as_view(), name='GoogleSearchConsole'),
    path('', views.submit_topic, name='submit_topic'),
    path('generate-assignment/', views.generate_assignment, name='generate_assignment'),
    path('generate-essay/', views.generate_essay, name='generate_essay'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]
