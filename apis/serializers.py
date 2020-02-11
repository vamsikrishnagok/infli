from rest_framework import serializers


from apis.models import Group,Images,GroupImage


class GroupSerializer(serializers.ModelSerializer):
    # popularityBar = serializers.Field(source='popularityBar')

    class Meta:
        model = Group
        fields = ("id","flickr_id","name","member_count","image_count","description")


class GroupImageSerializer(serializers.ModelSerializer):
    # popularityBar = serializers.Field(source='popularityBar')

    class Meta:
        model = GroupImage
        fields = ("image_id",)


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ("id","title","description","image")