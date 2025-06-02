from .models import Column

def columns_context(request):
    return {
        'all_columns': Column.objects.all()
    }