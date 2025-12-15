from django.db import transaction
from django.core.cache import cache
from .models import BaseUser


def create_user(*, username: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(username=username, password=password)


@transaction.atomic
def register(*, username: str, password: str) -> BaseUser:
    user = create_user(username=username, password=password)
    # TODO: create wallet here too

    return user