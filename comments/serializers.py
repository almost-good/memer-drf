from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Comment
from votes.models import Vote


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    profile_flair = serializers.ReadOnlyField(source='owner.profile.flair')
    vote_id = serializers.SerializerMethodField()
    vote_value = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def _get_user_vote(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            post_ct = ContentType.objects.get_for_model(Comment)
            vote = Vote.objects.filter(
                owner=user, content_type=post_ct, object_id=obj.id
            ).first()
            return vote
        return None
    
    def get_vote_id(self, obj):
        vote = self._get_user_vote(obj)
        return vote.id if vote else None # type: ignore
    
    def get_vote_value(self, obj):  
        vote = self._get_user_vote(obj)
        return vote.value if vote else None
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'owner',
            'is_owner',
            'profile_id',
            'profile_image',
            'profile_flair',
            'post',
            'created_at',
            'updated_at',
            'content',
            'vote_id',
            'vote_value',
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for Comment model used in detail view.
    """
    
    post = serializers.ReadOnlyField(source='post.id')
