from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
# import products.models
# custom user manager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=250, null=True)
    work = models.CharField(max_length=250, null=True)
    experience = models.CharField(max_length=250, null=True)
    rememberMe = models.BooleanField(default=False)
    education = models.CharField(max_length=200, null=True)
    about = models.CharField(max_length=500, null=True)
    bio = models.CharField(max_length=1000, null=True)
    linkedIn = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=200, null=True)
    twitter = models.CharField(max_length=200, null=True)
    facebook = models.CharField(max_length=200, null=True)
    number = models.IntegerField(null=True)
    profilePic = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likedPosts = models.ManyToManyField(
        "products.Product", blank=True, related_name='liked')
    savedPosts = models.ManyToManyField(
        "products.Product", blank=True, related_name='saved')
    likedComments = models.ManyToManyField(
        "products.Comment", blank=True, related_name='likedComment')
    dislikedComments = models.ManyToManyField(
        "products.Comment", blank=True, related_name='dislikedComment')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserFollowing(models.Model):

    user_id = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE, null=True)
    following_user_id = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        f"{self.user_id} follows {self.following_user_id}"
