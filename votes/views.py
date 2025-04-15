from rest_framework import generics, permissions
from memer_drf.permissions import IsOwnerOrReadOnly
from votes.models import Vote
from votes.serializers import VoteSerializer


class VoteList(generics.ListCreateAPIView):
    """
    List all votes or create a new vote.
    """
    
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Vote.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)