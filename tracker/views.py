from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ShiftForm, ShiftUpdateForm, DowntimeForm

from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
from .models import UserProfile, Shift, Downtime

from django.utils import timezone

import plotly.express as px
from plotly.offline import plot


# Create your views here.

def Login_Page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Account Non-existent")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password Incorrect")

    
    context = {"page":page}
    return render(request, "login_register.html", context)




def Register_Page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].lower()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            shift_type = form.cleaned_data["shift_type"]
            job = form.cleaned_data["job_type"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('register')


            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create linked UserProfile
            UserProfile.objects.create(
                user=user,
                shift_type=shift_type,
                job=job
            )
            login(request, user)


            messages.success(request, "Account created successfully!")
            return redirect("home")  # redirect to login page
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = UserForm()  

    context = {'form': form}
    return render(request, 'login_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')



def Home_Page(request):
    if not request.user.is_authenticated:
        return redirect('register')

    user = request.user
    user_shifts = Shift.objects.filter(user=user).order_by('id')

    chart = "<p>No production data yet.</p>"

    if user_shifts.exists():
        x = [f"Shift {i+1}" for i in range(len(user_shifts))]
        y = [shift.Production_Percentage() for shift in user_shifts]

        fig = px.line(
            x=x,
            y=y,
            title="Production Over Time",
            markers=True
        )
        fig.update_layout(
            yaxis_title="Production %",
            xaxis_title="Shift"
        )
        fig.update_traces(
            hovertemplate='Shift: %{x}<br>Production: %{y}%<extra></extra>'
        )

        chart = plot(fig, output_type='div')

    # Assign shift numbers
    for index, shift in enumerate(user_shifts, start=1):
        shift.shift_number = index

    user_shifts = reversed(list(user_shifts))

    form = ShiftForm()

    try:
        user_profile = UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        user_profile = None

    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            duty = form.cleaned_data['duty']
            shift = Shift.objects.create(duty=duty, user=user)
            return redirect('shift', pk=shift.id)

    context = {
        "profile": user_profile,
        "form": form,
        "user_shifts": user_shifts,
        "chart": chart,
    }

    return render(request, 'home_page.html', context)




def shift_page(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    form = ShiftUpdateForm(instance=shift)
    downtime_form = DowntimeForm()
    shift_downtime = Downtime.objects.filter(shift=shift)


    
    # --- Time logic ---
    now = timezone.now()
    elapsed = (shift.end_time or now) - shift.start_time
    hours_worked = elapsed.total_seconds() / 3600

    user_shifts = Shift.objects.filter(user=request.user).order_by('start_time')
    shift_number = user_shifts.filter(id__lte=shift.id).count()

    if request.method == "POST":
        form = ShiftUpdateForm(request.POST, instance=shift)


        if form.is_valid():
            move_type = form.cleaned_data["move_type"]

            if move_type == "regular":
                shift.regular_move += 1
            elif move_type == "long":
                shift.long_move += 1
            elif move_type == "pallete":
                shift.pallet_return += 1

            shift.save()
            return redirect('shift', pk=shift.pk)
    

    context = {"shift": shift, "form": form, "hours_worked": round(hours_worked,2), "production_rate": shift.Production_Percentage, "downtime_form": downtime_form, "shift_downtime": shift_downtime, "shift_number": shift_number}
    return render(request, 'shift.html', context)


def end_shift(request,pk): 
    shift = Shift.objects.get(pk=pk)
    shift.end_time = timezone.now()
    shift.save()
    return redirect('home')


def add_downtime(request, pk):
    shift = Shift.objects.get(pk=pk)
    if request.method == "POST":
        form = DowntimeForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["reason"]
            duration = form.cleaned_data["duration"]

            Downtime.objects.create(
                shift=shift,
                reason=reason,
                duration=duration
            )
            
            shift.downtime_minutes += duration
            shift.save()
            return redirect('shift', pk=shift.id)
            

