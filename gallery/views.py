from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Photo

class PhotoListView(ListView):
    model = Photo
    paginate_by = 6*4

class PhotoDetailView(DetailView):
    model = Photo
