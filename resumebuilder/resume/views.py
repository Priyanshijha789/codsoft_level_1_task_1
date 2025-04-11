from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Resume

def home(request):
    resume = None
    if request.user.is_authenticated:
        resume = Resume.objects.filter(user=request.user).first()
    return render(request, 'resume/home.html', {'resume': resume})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'resume/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'resume/dashboard.html')
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume
from django.contrib.auth.decorators import login_required

@login_required
def create_resume(request):
    try:
        resume = Resume.objects.get(user=request.user)
        form = ResumeForm(instance=resume)
    except Resume.DoesNotExist:
        resume = None
        form = ResumeForm()

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('resume_detail', resume_id=resume.id)

    return render(request, 'resume/create_resume.html', {'form': form})

from .models import Resume

@login_required
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user)

    return render(request, 'resume/my_resumes.html', {'resumes': resumes})
from django.shortcuts import get_object_or_404

from .models import Resume, Education

@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    education = Education.objects.filter(user=request.user)
    experience = Experience.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)

    return render(request, 'resume/resume_detail.html', {
        'resume': resume,
        'education': education,
        'experience': experience,
        'skills': skills,
        'projects': projects
    })

from .forms import EducationForm
from .models import Resume
from django.shortcuts import get_object_or_404

@login_required
def add_education(request):
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        return redirect('create_resume')  # Or your resume creation page

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('resume_detail', resume_id=resume.id)
    else:
        form = EducationForm()

    return render(request, 'resume/add_education.html', {
        'form': form,
        'resume': resume
    })

from .forms import ExperienceForm
from .models import Experience
@login_required
def add_experience(request):
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        return redirect('create_resume')

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            return redirect('resume_detail', resume_id=resume.id)
    else:
        form = ExperienceForm()

    return render(request, 'resume/add_experience.html', {'form': form, 'resume': resume})

from .forms import SkillForm
from .models import Skill
@login_required
def add_skill(request):
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        return redirect('create_resume')

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('resume_detail', resume_id=resume.id)
    else:
        form = SkillForm()

    return render(request, 'resume/add_skill.html', {'form': form, 'resume': resume})

from .forms import ProjectForm
from .models import Project

@login_required
def add_project(request):
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        return redirect('create_resume')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('resume_detail', resume_id=resume.id)
    else:
        form = ProjectForm()

    return render(request, 'resume/add_project.html', {'form': form, 'resume': resume})

from .utils import render_to_pdf
from .models import Resume, Education, Experience, Skill
from django.conf import settings

from django.templatetags.static import static
@login_required
def download_resume_pdf(request):
    resume = get_object_or_404(Resume, user=request.user)
    education = Education.objects.filter(user=request.user)
    experience = Experience.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    context = {
        'resume': resume,
        'education_list': education,
        'experience_list': experience,
        'skills': skills,
        'projects': projects,
        'media_url': settings.MEDIA_URL,
    }

    return render_to_pdf('resume/pdf_template.html', context)
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')
def get_absolute_url(self):
    return reverse('resume_detail', args=[str(self.id)])
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'resume/login.html'
