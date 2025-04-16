from django.db.models import Count, Sum, Case, When, IntegerField
from rest_framework import generics, permissions, filters
from memer_drf.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


VOTE_SCORE_EXPR = Sum(
    Case(
        When(vote__value=1,  then=1),
        When(vote__value=-1, then=-1),
        default=0,
        output_field=IntegerField(),
    )
)


class CommentList(generics.ListCreateAPIView):
    """
    List all comments or create a new comment.
    """
    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    queryset = Comment.objects.annotate(
        vote_count = Count("vote", distinct=True),
        vote_score = VOTE_SCORE_EXPR,
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
        vote_score = VOTE_SCORE_EXPR,
    ).order_by("-created_at")
