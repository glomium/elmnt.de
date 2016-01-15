from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Photo

class PhotoListView(ListView):
    model = Photo
    paginate_by = 6*4

    def get_context_data(self, **kwargs):
        kwargs.update({'size': (245, 141)})
        return super(PhotoListView, self).get_context_data(**kwargs)

class PhotoDetailView(DetailView):
    model = Photo
