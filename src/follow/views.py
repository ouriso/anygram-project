from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.views.generic import ListView

from recipes.models import Recipe

User = get_user_model()


class FollowListView(LoginRequiredMixin, ListView):
    paginate_by = 3
    template_name = 'follow_index.html'

    def get_queryset(self):
        queryset = list(self.request.user.follow.all())
        for i in queryset:
            print(i)
        # queryset = []
        # for user in follower.follow:
        #     queryset.append(user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['title'] = 'Ваши подписки'
        return context
