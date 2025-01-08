from django.urls import path
from .views import ReactionListCreateAPIView

urlpatterns = [
    path('reactions/', ReactionListCreateAPIView.as_view(), name='reaction-list-create'),
]
