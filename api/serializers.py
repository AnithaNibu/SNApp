from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    comment_like=serializers.CharField(read_only=True)
    comment_like_count=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields="__all__"
class PostSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    post_like=serializers.CharField(read_only=True)
    post_like_count=serializers.CharField(read_only=True)
    post_comments=CommentSerializer(read_only=True,many=True)
    class Meta:
        model=Posts
        fields="__all__"


