from rest_framework import viewsets, permissions, status

from freelance.advert.models import Advert, AdvertFile, Comment
from freelance.advert import serializers, permissions as custom_perm


class AdvertViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertSerializer
    permission_classes = [custom_perm.IsCustomer, custom_perm.IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class FileViewSet(viewsets.ModelViewSet):
    queryset = AdvertFile.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [custom_perm.IsExecutor]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
