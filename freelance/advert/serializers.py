from rest_framework import serializers

from freelance.advert.models import Advert, AdvertFile, Comment


class AdvertSerializer(serializers.ModelSerializer):
    files = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Advert
        fields = ["id", "title", "executor", "description", "award", "status",
                  "created", "files"]

    def create(self, validated_data):
        if "files" not in validated_data:
            return super(AdvertSerializer, self).create(validated_data)

        files = validated_data.pop("files")
        advert_instance = super(AdvertSerializer, self).create(validated_data)
        for file in files:
            AdvertFile.objects.create(user=advert_instance.customer, file=file,
                                      advert=advert_instance)
        return advert_instance


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertFile
        fields = ["id", "file", "created"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created"]
