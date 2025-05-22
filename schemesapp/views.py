from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm, AddEmployee
from .models import Feedback, Notification
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
# Create your views here.

def home(request):
    notifications = []

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        print("User:", request.user)
        print("Notifications:", notifications)
    return render(request, 'home.html', {'notifications': notifications})

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback.html', {'form': form})

@login_required
def view_feedback(request):

    scheme_filter = request.GET.get('scheme', '')  # e.g., 'BBBP', 'SBA', 'NIL' or empty
    replied_filter = request.GET.get('replied', '')  # 'yes', 'no', or empty

    
    if  request.user.groups.filter(name='Employee').exists():
        feedbacks = Feedback.objects.select_related('user').order_by("-submitted_at")
    else :
        feedbacks = Feedback.objects.filter(user=request.user).order_by("-submitted_at")

    if request.user.groups.filter(name='Employee').exists():
        feedbacks = Feedback.objects.select_related('user').order_by("-submitted_at")
    else:
        feedbacks = Feedback.objects.filter(user=request.user).order_by("-submitted_at")

    # Filter by scheme if selected
    if scheme_filter and scheme_filter in dict(Feedback.SCHEME_CHOICES).keys():
        feedbacks = feedbacks.filter(scheme=scheme_filter)

    # Filter by replied or not
    if replied_filter == 'yes':
        feedbacks = feedbacks.exclude(reply__isnull=True).exclude(reply__exact='')
    elif replied_filter == 'no':
        feedbacks = feedbacks.filter(reply__isnull=True) | feedbacks.filter(reply='')

    # Pass scheme choices to template for dropdown
    scheme_choices = Feedback.SCHEME_CHOICES


    return render(request, 'feedback/viewfeedback.html',{'feedbacks': feedbacks, 'scheme_choices': scheme_choices, 'selected_scheme': scheme_filter, 'selected_replied': replied_filter,})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to your home view name
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def add_employee(request):
    if request.method == 'POST':
        form =AddEmployee(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username= username)
                employee_group, created = Group.objects.get_or_create(name = 'Employee')
                user.groups.add(employee_group)
                user.save()
                messages.success(request, 'Employee Added')
                return redirect('add_employee')
            except User.DoesNotExist:
                form.add_error('username', 'User with this name does not exist.')
    else:
            form = AddEmployee()
    return render(request, 'addEmployee.html', {'form': form})

@login_required
@user_passes_test(is_employee)
@login_required
def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        feedback.reply = reply
        feedback.save()
    
        Notification.objects.create(
            user=feedback.user,
            message=f"Your feedback on {feedback.scheme} has been replied to.",
            link=f"/viewfeedbacks/#{feedback.id}"
        )

        return redirect('view_feedbacks')
    return render(request, 'feedback/reply_feedback.html', {'feedback': feedback})



