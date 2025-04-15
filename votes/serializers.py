from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Vote
from posts.models import Post
from comments.models import Comment


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.
    """
    
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Vote
        fields = [
            'id',
            'owner',
            'content_type',
            'object_id',
            'value',
            'created_at',
        ]
    
    def validate_value(self, value):
        if value not in [1, -1]:
            raise serializers.ValidationError(
                "Vote must be 1 (upvote) or -1 (downvote)."
            )
        return value
    
    def validate(self, data):
        """
        Validate that the content type is either Post or Comment.
        """
        
        allowed_models = [Post, Comment]
        allowed_cts = [
            ContentType.objects.get_for_model(model) for model in allowed_models
        ]
        if data['content_type'] not in allowed_cts:
            raise serializers.ValidationError(
                "Votes can only be cast on posts or comments."
            )
        return data
