from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager as BUM


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class BaseUserManager(BUM):
    def create_user(self, username, password=None, is_active=True, is_admin=False):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            username=username,
            is_active=is_active,
            is_admin=is_admin
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
            is_active=True,
            is_admin=True,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user