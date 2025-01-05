from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string,json


# Create your models here.

USER_TYPE_CHOICES = [
    ('ADMIN', 'admin'),
    ('TURF', 'turf'),
    ('PUBLIC', 'public'),

]

STATUS_CHOICE = (
    ("ACTIVE", "Active"),
    ("INACTIVE", "Inactive"),  
)


class Userprofile(AbstractUser):
    # username
    # password
    user_type=models.CharField( max_length=50,null=False,blank=False,choices=USER_TYPE_CHOICES)
    status = models.CharField(max_length=20, null=True, choices=STATUS_CHOICE)
    is_active = models.BooleanField(null=False,blank=True,default=True)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField( 'auth.Group', related_name='userprofile_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='userprofile_permissions', blank=True)

class Token(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(
        Userprofile,
        related_name="auth_tokens",
        on_delete=models.CASCADE, 
        verbose_name="user",
        unique=True,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    session_dict = models.TextField(null=False, default="{}")
    dict_ready = False
    data_dict = None

    def _init_(self, *args, **kwargs):
        self.dict_ready = False
        self.data_dict = None
        super(Token, self)._init_(*args, **kwargs)

    def generate_key(self):
        return "".join(
            random.choice(
                string.ascii_lowercase + string.digits + string.ascii_uppercase
            )
            for i in range(40)
        )

    def save(self, *args, **kwargs):
        if not self.key:
            new_key = self.generate_key()
            while type(self).objects.filter(key=new_key).exists():
                new_key = self.generate_key()
            self.key = new_key
        return super(Token, self).save(*args, **kwargs)

    def read_session(self):
        if self.session_dict == "null":
            self.data_dict = {}
        else:
            self.data_dict = json.loads(self.session_dict)
        self.dict_ready = True

    def update_session(self, tdict, save=True, clear=False):
        if not clear and not self.dict_ready:
            self.read_session()
        if clear:
            self.data_dict = tdict
            self.dict_ready = True
        else:
            for key, value in tdict.items():
                self.data_dict[key] = value
        if save:
            self.write_back()

    def set(self, key, value, save=True):
        if not self.dict_ready:
            self.read_session()
        self.data_dict[key] = value
        if save:
            self.write_back()

    def write_back(self):
        self.session_dict = json.dumps(self.data_dict)
        self.save()

    def get(self, key, default=None):
        if not self.dict_ready:
            self.read_session()
        return self.data_dict.get(key, default)

    def _str_(self):
        return str(self.user) if self.user else str(self.id)











