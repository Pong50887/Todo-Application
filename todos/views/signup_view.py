from django.contrib.auth import login
from django.shortcuts import redirect, render
from ..forms import RegisterForm


def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in the user after registration
            return redirect('todo_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})
