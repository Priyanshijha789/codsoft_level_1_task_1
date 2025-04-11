from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('my/', views.my_resumes, name='my_resumes'),
    path('<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('add-education/', views.add_education, name='add_education'),
    path('add-experience/', views.add_experience, name='add_experience'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('add-project/', views.add_project, name='add_project'),
    path('download-pdf/', views.download_resume_pdf, name='download_resume_pdf'),
    
]


