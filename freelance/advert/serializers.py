from rest_framework import serializers

from freelance.advert.models import Advert, AdvertFile, Comment, AdvertResponse
from freelance.users.serializers import CustomUserSerializer


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ["id", "title", "executor", "description", "award", "status",
                  "created"]


class FileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    advert = AdvertSerializer(read_only=True)

    class Meta:
        model = AdvertFile
        fields = ["id", "file", "user", "advert", "created"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "text", "parent", "created"]


class AdvertResponseSerializer(serializers.ModelSerializer):
    executor = CustomUserSerializer(read_only=True)
    advert = AdvertSerializer(read_only=True)

    class Meta:
        model = AdvertResponse
        fields = ["id", "executor", "advert", "text", "created"]