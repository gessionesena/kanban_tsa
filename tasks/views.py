from django.urls import reverse_lazy
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Column, Task, Activity
from .forms import TaskMoveForm, TaskUpdateForm, TaskCreateForm




class KanbanBoardView(TemplateView):
    template_name = 'kanban_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search', '').strip()

        columns = Column.objects.all()

        # Adiciona uma lista de tarefas filtradas em cada coluna
        for column in columns:
            if query:
                tasks = column.task_set.filter(title__icontains=query).order_by('-updated_at')
            else:
                tasks = column.task_set.all().order_by('-updated_at')
            column.tasks_filtered = tasks

        context['columns'] = columns
        context['query'] = query

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('kanban_board')


class TaskMoveView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskMoveForm
    template_name = 'task_move.html'
    success_url = reverse_lazy('kanban_board')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task_edit.html'

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('kanban_board')


class BulkCreateTaskView(View):
    def get(self, request):
        activities = Activity.objects.all()
        columns = Column.objects.all()
        return render(request, 'bulk_create_tasks.html', {
            'activities': activities,
            'columns': columns
            })
    
    def post(self, request):
        action = request.POST.get('action')
        
        #Ação para adicionar atividades a lista de atividades com checkbox
        if action == 'add':
            title = request.POST.get('new_activity_title')
            if title:
                Activity.objects.create(title=title)
                messages.success(request, 'Atividade adicionada com sucesso.')
            else:
                messages.error(request, 'Título da atividade não pode ser vazio.')
            return redirect('bulk_create_tasks')

        #Ação para identificar se é para adicionar as atividades selecionadas às tarefas ou excluir as atividades selecionadas
        selected_ids = request.POST.getlist('selected_activities')

        if not selected_ids:
            messages.error(request, 'Nenhuma atividade selecionada.')
            return redirect('bulk_create_tasks')
        
        if action == 'delete':
            Activity.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Atividades excluídas com sucesso.')
        
        elif action == 'create':
            column_id = request.POST.get('column_id')
            if not column_id:
                messages.error(request, 'Selecione uma coluna para criar as tarefas.')
                return redirect('bulk_create_tasks')
            column = get_object_or_404(Column, id=column_id)
            activities = Activity.objects.filter(id__in=selected_ids)
            for activity in activities:
                Task.objects.create(title=activity.title, column=column)

             # Deletamos as atividades usadas para criar tarefas
            activities.delete()
            
            messages.success(request, 'Tarefas criadas  e atividades removidas com sucesso.')

        return redirect('bulk_create_tasks')



class ColumnTaskListView(ListView):
    model = Task
    template_name = 'column_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        pk = self.kwargs.get('pk')  # Captura o ID da coluna a partir da URL
        query = self.request.GET.get('search', '').strip()
        queryset = Task.objects.filter(column_id=pk)
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset.order_by('-updated_at') 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['column'] = Column.objects.get(pk=self.kwargs['pk'])
        context['query'] = self.request.GET.get('search', '').strip()
        return context
        


           
    
