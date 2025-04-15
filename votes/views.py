from rest_framework import generics, permissions, status
from rest_framework.response import Response
from memer_drf.permissions import IsOwnerOrReadOnly
from votes.models import Vote
from votes.serializers import VoteSerializer


class VoteList(generics.ListCreateAPIView):
    """
    List all votes and toggle a vote (smart create/delete/update)
    """
    
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Vote.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a smart toggle for votes:
        
        - Vote already exists: update it.
        - Vote does not exist: create it.
        - Vote value is the same: delete it.
        """
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        vote, created = Vote.objects.get_or_create(
            owner=request.user,
            content_type=data['content_type'],
            object_id=data['object_id'],
            defaults={'value': data['value']}
        )

        if not created:
            if vote.value == data['value']:
                vote.delete()
                return Response(
                    {'detail': 'Vote removed.'}, 
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                vote.value = data['value']
                vote.save()
                return Response(
                    self.get_serializer(vote).data, 
                    status=status.HTTP_200_OK
                )

        return Response(
            self.get_serializer(vote).data, 
            status=status.HTTP_201_CREATED
        )
