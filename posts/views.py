from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from memer_drf.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    List all posts or create a new post.
    """
    
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """
    
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()

