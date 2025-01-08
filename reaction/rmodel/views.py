from rest_framework import generics
from .models import Reaction
from .serializer import ReactionSerializer

class ReactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
