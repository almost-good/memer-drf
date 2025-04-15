from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from memer_drf.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListCreateAPIView):
    """
    List all profiles.
    """
    
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a profile instance.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()

