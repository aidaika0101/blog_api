from rest_framework import serializers

from like.models import Like, Favorite


class LikeUserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Like
        exclude = ('post', )


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Like
        fields = '__all__'


    def validate(self, attrs):
        user = self.context['request'].user
        post = attrs['post']
        if user.likes.filter(post=post).exists():
            raise serializers.ValidationError(
                'You already liked this post!'
            )
        return attrs



class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'post')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        preview = instance.post.preview
        repr['post_preview'] = preview.url if preview else None
        return repr
