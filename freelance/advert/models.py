from django.contrib.auth import get_user_model
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

User = get_user_model()

STATUS = (
    ('WAI', 'Waiting'),
    ('INP', 'In Progress'),
    ('COM', 'Complete'),
    ('CAN', 'Canceled'),
)


class Advert(models.Model):
    customer = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='executor', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    award = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    status = models.CharField(max_length=3, choices=STATUS, default='WAI')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.customer.full_name} - {self.title}'


def file_path(instance, filename):
    return '/'.join(['files', f'{instance.advert.id} {instance.advert.title}', filename])


class AdvertFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_path)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.file.name}'


class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    text = models.TextField("comment content", max_length=5000)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.advert.title}"


class AdvertResponse(models.Model):
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.advert.title} - {self.executor.email}"
