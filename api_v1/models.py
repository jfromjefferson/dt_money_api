from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.


class Owner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username


class SysUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    title = models.CharField(max_length=60)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)


class Transaction(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    value = models.IntegerField()
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(
        choices=(
            ('deposit', 'Deposit'),
            ('withdrawal', 'Withdrawal')
        ),
        max_length=12
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.title
