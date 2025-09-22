from django.views.generic import TemplateView, DetailView, ListView
from main.models import Post


class IndexView(ListView):
    model = Post
    template_name = "main/index.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        show_all = self.request.GET.get("show_all")

        if show_all:
            return queryset
        else:
            return queryset[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_all'] = bool(self.request.GET.get('show_all'))

        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "main/details.html"
