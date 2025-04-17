from django.db.models import Count
from rest_framework import generics, permissions, filters
from memer_drf.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from utils.helper import get_vote_score_expr

class CommentList(generics.ListCreateAPIView):
    """
    List all comments or create a new comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Comment.objects.annotate(
        vote_count = Count("vote", distinct=True),
        vote_score = get_vote_score_expr('vote__value')
    ).order_by("-created_at")

    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'vote_count',
        'vote_score',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment instance.
    """

    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.annotate(
        vote_count = Count("vote", distinct=True),
        vote_score = get_vote_score_expr('vote__value')
    ).order_by("-created_at")
