from django.db import models
from django.core.mail import send_mail

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
# функция перевода на другой язык
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Genders(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
    
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        db_index=True,
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), db_index=True, unique=True, 
                              error_messages={'unique': _('user with this email address already exists')})
    
    first_name = models.CharField(_('first name'), max_length=45, blank=True)
    last_name = models.CharField(_('last name'), max_length=45, blank=True)

    gender = models.CharField(_('gender'), max_length=1, choices=Genders.choices, 
                              default=Genders.MALE, null=True, blank=True)
    birth_date = models.DateField(_('date of birth'), null=True, blank=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = 'user'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self) -> str:
        return self.email
