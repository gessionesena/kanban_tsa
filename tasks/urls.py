from django.urls import path
from . import views

urlpatterns = [
    path('', views.KanbanBoardView.as_view(), name='kanban_board'),
    path('activities_to_tasks/', views.BulkCreateTaskView.as_view(), name='bulk_create_tasks'),
    path('column/<int:pk>/tasks/',views.ColumnTaskListView.as_view(), name='column_tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/detail/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/move/', views.TaskMoveView.as_view(), name='task_move'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
]