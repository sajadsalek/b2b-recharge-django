from django.core.exceptions import ImproperlyConfigured

import os
from dotenv import load_dotenv
from dataclasses import dataclass, field

load_dotenv()

@dataclass(frozen=True)
class Config:
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL"))
    database_name: str = field(default_factory=lambda: os.getenv("DATABASE_NAME"))
    database_user: str = field(default_factory=lambda: os.getenv("DATABASE_USER"))
    database_password: str = field(default_factory=lambda: os.getenv("DATABASE_PASSWORD"))
    database_host: str = field(default_factory=lambda: os.getenv("DATABASE_HOST"))
    database_port: str = field(default_factory=lambda: os.getenv("DATABASE_PORT"))



    def __post_init__(self):
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                raise ImproperlyConfigured(f"{field_name.upper()} is missing in environment variables.")
