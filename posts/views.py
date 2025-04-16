from django.db.models import Count, Sum, Case, When, IntegerField
from rest_framework import generics, permissions, filters
from .models import Post
from .serializers import PostSerializer
from memer_drf.permissions import IsOwnerOrReadOnly


VOTE_SCORE_EXPR = Sum(
    Case(
        When(vote__value=1,  then=1),
        When(vote__value=-1, then=-1),
        default=0,
        output_field=IntegerField(),
    )
)


class PostList(generics.ListCreateAPIView):
    """
    List all posts or create a new post.
    """
    
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    queryset = Post.objects.annotate(
        comments_count=Count('comments', distinct=True),
        vote_count=Count("vote", distinct=True),
        vote_score=VOTE_SCORE_EXPR
    ).order_by('-created_at')
    
    filter_backends = [
        filters.OrderingFilter
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
        vote_score=VOTE_SCORE_EXPR
    ).order_by('-created_at')

