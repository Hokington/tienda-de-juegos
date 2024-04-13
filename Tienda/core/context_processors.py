from core.models import Categoria

def load_categorias(request):
    categorias = Categoria.objects.all()
    
    return {
        'categorias': categorias,
    }
