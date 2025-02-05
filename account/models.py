from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Номер телефона обязателен.")
        if not password:
            raise ValueError("Пароль обязателен.")

        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        verbose_name='Фамилия'
    )

    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        verbose_name='Номер телефона'
    )
    gender = models.CharField(
        max_length=1, 
        choices=[('M', 'Мужчина'), ('F', 'Женщина')], 
        blank=True, 
        null=True, 
        verbose_name='Пол'
    )
    birth_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Дата рождения'
    )

    password = models.CharField(
        max_length=128, 
        verbose_name='Пароль'
    )
    last_login = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Последний вход'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set',
        related_query_name='user',
        blank=True,
        verbose_name='Группы'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set',
        related_query_name='user',
        blank=True,
        verbose_name='Права доступа'
    )

    is_staff = models.BooleanField(
        default=False, 
        verbose_name='Статус персонала'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активен'
    )
    is_superuser = models.BooleanField(
        default=False, 
        verbose_name='Суперпользователь'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def clean(self):

        if self.birth_date and self.birth_date > date.today():
            raise ValidationError({'birth_date': 'Дата рождения не может быть в будущем.'})


        if self.gender and self.gender not in ['M', 'F']:
            raise ValidationError({'gender': 'Пол должен быть либо "Мужчина" (M), либо "Женщина" (F).'})
    
    def __str__(self) -> str:
        return self.phone_number
