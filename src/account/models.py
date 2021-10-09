from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password):
        """
        Creates and saves a normal user and return its object.
        """
        if not email:
            raise ValueError("Please enter an email address.")
        if not username:
            raise ValueError("Please enter a username.")
        if not password:
            raise ValueError("Please enter a password.")
        
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Creats and saves a superuser and return it's object.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

def get_default_profile_image():
    """
    Returns path to the default profile image.
    """
    return "pictures/default_profile_image.png"

def get_profile_image_filepath(self, filename):
    """
    Returns path to a users custom profile image. Used as the upload path of a profile image.
    """
    return "profile_images/" + str(self.pk) + "/profile_image.png"

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=25, unique=True)
    biography = models.CharField(max_length=255, blank=True, null=True, default="I'm tooo boring :((")
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)


    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()
    
    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index("profile_images/" + str(self.pk) + "/"):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True