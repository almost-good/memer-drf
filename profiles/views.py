from django.db.models import Count
from rest_framework import generics, filters

import posts
from .models import Profile
from .serializers import ProfileSerializer
from memer_drf.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListCreateAPIView):
    """
    List all profiles.
    """
    
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a profile instance.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()

