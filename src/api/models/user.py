from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from ..managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    STAFF = "staff"
    EMPLOYEE = "employee"
    EMPLOYER = "employer"
    PUBLIC = "public"
    USER_TYPE_CHOICES = [
        (STAFF, _("Staff")),
        (EMPLOYEE, _("Employee")),
        (EMPLOYER, _("Employer")),
        (PUBLIC, _("Public")),
    ]
    email = models.EmailField(_('email address'), db_index=True, blank=True)
    username = models.CharField(_("username"), max_length=100, db_index=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    user_type = models.CharField(_("user type"), max_length=10, choices=USER_TYPE_CHOICES, blank=False, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
