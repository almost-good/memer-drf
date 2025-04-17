from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from memer_drf.permissions import IsOwnerOrReadOnly
from utils.helper import get_vote_score_expr


class PostList(generics.ListCreateAPIView):
    """
    List all posts or create a new post.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.annotate(
        comments_count=Count('comments', distinct=True),
        vote_count=Count("vote", distinct=True),
        vote_score=get_vote_score_expr('vote__value')
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = {
        # user feed
        'owner__followed__owner__profile',
        # user voted posts
        'vote__owner__profile',
        # user posts
        'owner__profile',
    }
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'comments_count',
        'vote_count',
        'vote_score',
        'vote__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comments', distinct=True),
        vote_count=Count("vote", distinct=True),
        vote_score=get_vote_score_expr('vote__value')
    ).order_by('-created_at')
