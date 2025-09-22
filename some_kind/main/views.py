from django.views.generic import TemplateView, DetailView, ListView
from main.models import Post


class IndexView(ListView):
    model = Post
    template_name = "main/index.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        return queryset.all()

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "main/details.html"
