from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.views import View
from django.views.generic.edit import FormMixin
from main.models import Post
from main.forms import SendMessageForm
from django.urls import reverse


class IndexView(FormMixin,ListView):
    model = Post
    form_class = SendMessageForm
    template_name = "main/index.html"

    def get_success_url(self):
        return reverse("main:index")

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        show_all = self.request.GET.get("show_all")

        if show_all:
            return queryset
        else:
            return queryset[:4]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            if not form.name and self.request.user.is_authenticated:
                form.name = self.request.user.username
            form.save()
            return self.form_valid(form)
        else:
            self.object_list = self.get_queryset()
            return self.form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            posts = context['object_list']
            posts_data = [{
                'id': post.id,
                'name': post.name,
                'slug': post.slug,
                'description': post.description,
                'image_url': post.image.url if post.image else ''
            } for post in posts]
            return JsonResponse({'posts': posts_data})
        else:
            return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_all'] = bool(self.request.GET.get('show_all'))
        context['form'] = self.get_form()

        return context

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "main/details.html"
