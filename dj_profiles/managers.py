from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, first_name, last_name, date_birth, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set!')
        if not name:
            raise ValueError('The given name must be set!')
        if len(name) < 3:
            raise ValueError('Few characters!')
        if not first_name and not last_name:
            raise ValueError('The given first_name and last_name must be set!')
        if not date_birth:
            raise ValueError('The given date_birth must be set!')

        email = self.normalize_email(email)

        user = self.model(email=email, name=name, first_name=first_name, last_name=last_name, date_birth=date_birth,
                          **extra_fields)
        user.password = make_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(self, email, name, first_name, last_name, date_birth, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, name, first_name, last_name, date_birth, password, **extra_fields)

    def create_superuser(self, email, name, first_name, last_name, date_birth, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, name, first_name, last_name, date_birth, password, **extra_fields)
