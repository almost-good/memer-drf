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
        Validate that the content type and object ID are valid.
        """
        
        allowed_models = [Post, Comment]
        allowed_cts = [
            ContentType.objects.get_for_model(model) for model in allowed_models
        ]
        
        content_type = data['content_type']
        object_id = data['object_id']
        
        if data['content_type'] not in allowed_cts:
            raise serializers.ValidationError(
                "Votes can only be cast on posts or comments."
            )
        
        try:
            content_type.get_object_for_this_type(pk=object_id)
        except content_type.model_class().DoesNotExist:
            raise serializers.ValidationError(
                "The object you're trying to vote on does not exist."
            )
        
        return data
