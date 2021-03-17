from .views import FollowListView
from django.urls import path

urlpatterns = [
    path('', FollowListView.as_view(), name='index_follow'),
]
