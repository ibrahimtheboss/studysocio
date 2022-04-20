from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import Signup
# Create your views here.


def frontpage(request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == "POST":
        form = Signup(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.studysocioprofile.designation = form.cleaned_data.get('designation')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('frontpage')
    else:
        form = Signup()

    return render(request, 'core/signup.html', {'form': form})
