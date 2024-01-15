
from rest_framework import serializers

from comment.serializers import CommentSerializer
from post.models import Post, PostImage


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'owner_username', 'category_name', 'category', 'preview')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
        return repr





class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        images = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        post_images = [PostImage(image=image, post=post) for image in images]
        PostImage.objects.bulk_create(post_images)
        return post

class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)
    # comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['comments_count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        repr = super().to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
        return repr










