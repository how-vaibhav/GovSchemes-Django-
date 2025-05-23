from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import FeedbackForm, AddEmployee, Add_Scheme_Form, User_Details_Form
from .models import Feedback, Notification, Scheme, UserDetails
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
import json, requests
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    if scheme_filter:
        feedbacks = feedbacks.filter(scheme__name=scheme_filter)

    # Filter by replied or not
    if replied_filter == 'yes':
        feedbacks = feedbacks.exclude(reply__isnull=True).exclude(reply__exact='')
    elif replied_filter == 'no':
        feedbacks = feedbacks.filter(reply__isnull=True) | feedbacks.filter(reply='')

    # Pass scheme choices to template for dropdown
    scheme_choices = [(name, name) for name in Scheme.objects.values_list('name', flat=True)]

    total_feedbacks = feedbacks.count()
    total_replied = feedbacks.exclude(reply__isnull=True).exclude(reply__exact='').count()
    total_unreplied = (feedbacks.filter(reply__isnull=True) | feedbacks.filter(reply='')).count()



    return render(request, 'feedback/viewfeedback.html',{'feedbacks': feedbacks, 'scheme_choices': scheme_choices, 'selected_scheme': scheme_filter, 'selected_replied': replied_filter, 'total_feedbacks':total_feedbacks, 'total_replied':total_replied, 'total_unreplied':total_unreplied,})

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

@csrf_exempt
def translate_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get("text","")
        source = data.get("source","en")
        target = data.get("target","")

        response = requests.post("http://localhost:5000/translate", json={
            "q": text,
            "source" : source,
            "target":target,
            "format":"text"
        })

        if response.status_code == 200:
            return JsonResponse({"translatedText": response.json().get("translatedText")})
        else:
            return JsonResponse({"error": "Translation failed"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def scheme_list(request):
    schemes = Scheme.objects.all()
    return render(request, 'scheme_list.html', {'schemes': schemes})

def scheme_detail(request, pk):
    scheme = get_object_or_404(Scheme, pk=pk)

    feedbacks = Feedback.objects.all().order_by('-submitted_at')  # get all feedback for this scheme

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.scheme = scheme
            feedback.user = request.user
            feedback.save()
            return redirect('scheme_detail', pk=pk)  # Redirect to avoid resubmission on refresh
    else:
        form = FeedbackForm()

    context = {
        'scheme': scheme,
        'feedbacks': feedbacks,
        'form': form,
    }
    return render(request, 'schemes/scheme_detail.html', context)

@login_required
@user_passes_test(is_employee)
def scheme_input(request):
    if request.method == 'POST':
        form = Add_Scheme_Form(request.POST)
        if form.is_valid():
            scheme = form.save()
            messages.success(request, "Feedback Added.")
            return redirect('scheme_list')
    else:
        form = Add_Scheme_Form()    
    return render(request, 'schemesapp/add_scheme.html', {'form': form})

@login_required
def user_detail_input(request):
    try:
        details = UserDetails.objects.get(user=request.user)
        return redirect('view_user_details')  # Redirect to a view-only page if already submitted
    except UserDetails.DoesNotExist:
        if request.method == 'POST':
            form = User_Details_Form(request.POST)
            if form.is_valid():
                user_details = form.save(commit=False)
                user_details.user = request.user
                user_details.save()
                messages.success(request, "User Data Added.")
                return redirect('home')
        else:
            form = User_Details_Form()    
        return render(request, 'user_detail.html', {'form': form})

@login_required
def scheme_eligibility(request, pk):
    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail')
    
    scheme = get_object_or_404(Scheme, pk=pk)

    is_eligible = scheme.is_user_eligible(details)

    return render(request, 'eligibility.html', {'details': details, 'scheme':scheme, 'is_eligible':is_eligible})

@login_required
def check_all_eligibility(request):
    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail')  # Force user to fill details first

    eligible_schemes = []

    all_schemes = Scheme.objects.all()
    for scheme in all_schemes:
        if scheme.is_user_eligible(details):
            eligible_schemes.append(scheme)

    return render(request, 'eligible_schemes.html', {
        'eligible_schemes': eligible_schemes,
        'total': len(eligible_schemes),
    })

@login_required
def view_user_details(request):
    user = request.user

    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail')

    fields = [(field.verbose_name.title(), getattr(details, field.name)) for field in UserDetails._meta.fields if field.name != 'id']

    return render(request, 'view_user_details.html', {'fields': fields})

@login_required
def edit_user_details(request):
    details = UserDetails.objects.get(user=request.user)
    if request.method == 'POST':
        form = User_Details_Form(request.POST, instance=details)
        if form.is_valid():
            form.save()
            return redirect('view_user_details')
    else:
        form = User_Details_Form(instance=details)
    return render(request, 'edit_user_details.html', {'form': form})

@receiver(post_save, sender=Scheme)
def notify_users_on_new_scheme(sender, instance, created, **kwargs):
    if created:
        scheme = instance

        for user_detail in UserDetails.objects.all():
            eligible = scheme.is_user_eligible(user_detail)
            message = f"New scheme '{scheme.name}' added. You are {'eligible' if eligible else 'not eligible'}."

            Notification.objects.create(
                user=user_detail.user,  # Assuming UserDetails links to User
                message=message,
                scheme=scheme,
                is_read=False,
            )