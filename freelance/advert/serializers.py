from rest_framework import serializers

from freelance.advert.models import Advert, AdvertFile, Comment, AdvertResponse


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ["id", "title", "executor", "description", "award", "status",
                  "created"]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertFile
        fields = ["id", "file", "advert", "created"]


class ActionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertFile
        fields = ["file"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "text", "parent", "created"]


class AdvertResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertResponse
        fields = ["id", "executor", "advert", "text", "created"]


class ActionAdvertResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertResponse
        fields = ["text"]
