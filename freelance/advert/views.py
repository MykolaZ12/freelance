from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from freelance.advert.models import Advert, AdvertFile, Comment, AdvertResponse
from freelance.advert import serializers, permissions as custom_permissions


class AdvertViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertSerializer
    permission_classes = [custom_permissions.IsCustomer, custom_permissions.IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(methods=['post'], detail=True, url_path='file', url_name='upload_file',
            serializer_class=serializers.ActionFileSerializer)
    def upload_file(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, advert_id=pk)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='file/bulk_create',
            url_name='upload_many_files', serializer_class=serializers.ActionFileSerializer)
    def upload_many_files(self, request, pk=None):
        try:
            files = request.FILES.getlist('file')
        except KeyError:
            raise ParseError('Request has no resource file attached')
        for file in files:
            serializer = self.serializer_class(data={"file": file})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user, advert_id=pk)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='response', url_name='response',
            permission_classes=[custom_permissions.IsExecutor],
            serializer_class=serializers.ActionAdvertResponseSerializer)
    def response(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(executor=self.request.user, advert_id=pk)
        return Response(status=status.HTTP_201_CREATED)


class FileViewSet(viewsets.ModelViewSet):
    queryset = AdvertFile.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [custom_permissions.IsCustomer, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdvertResponseViewSet(viewsets.ModelViewSet):
    queryset = AdvertResponse.objects.all()
    serializer_class = serializers.AdvertResponseSerializer
    permission_classes = [custom_permissions.IsExecutor]

    def perform_create(self, serializer):
        serializer.save(executor=self.request.user)
