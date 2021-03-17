from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.views.generic import ListView

from recipes.models import Recipe

User = get_user_model()


class FollowListView(LoginRequiredMixin, ListView):
    paginate_by = 9
    template_name = 'follow_index.html'

    def get_queryset(self):
        queryset = Recipe.objects.filter(author__in=self.request.user.follow.all())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['title'] = 'Ваши подписки'
        return context
