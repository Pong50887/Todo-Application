from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from todos.models import Todo
from todos.forms import TodoForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
import json


@csrf_exempt
@login_required
def update_status_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            todo_id = data.get('id')
            new_status = data.get('status')

            if new_status not in ['pending', 'in_progress', 'done']:
                return JsonResponse({'error': 'Invalid status'}, status=400)

            todo = get_object_or_404(Todo, id=todo_id, user=request.user)
            todo.status = new_status
            todo.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    status_columns = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    return render(request, 'todos/todo_list.html', {
        'todos': todos,
        'status_columns': status_columns,
    })

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/add_todo.html', {'form': form})

@login_required
def update_todo_status(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if todo.status == 'in_progress':
        todo.status = 'done'
    else:
        todo.status = 'in_progress'

    todo.save()
    return redirect('todo_list')

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    messages.success(request, "Todo deleted successfully.")
    return redirect('todo_list')


@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully.")
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)

    return render(request, 'todos/edit_todo.html', {'form': form})
