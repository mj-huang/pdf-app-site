import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
#from django.db.models.signals import post_save
from django.conf import settings
from .validators import validate_file_extension, user_directory_path, directory_path_for_ref_letter
#from django.utils.translation import ugettext_lazy as _

# Extending the base User manager that Django uses for its original UserManager.
class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email, date of
    birth and password.
    """
    use_in_migration = True
    
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            email,
            password = password,
        )

        user.is_admin = True
        user.save(using = self._db)

        return user

    def get_queryset(self):
        return super(UserManager, self).get_queryset()
    # Defining the same 3 methods that the original Django UserManager has,
    # and not using username in either of those methods.

class Sponsor(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default=uuid.uuid4,
        editable = False
    )

    email = models.EmailField(
        max_length = 255,
        verbose_name = 'email address',
        unique = True
    )

    first_name = models.CharField(max_length=30, verbose_name='First Name', blank=True)
    last_name = models.CharField(max_length=30, verbose_name='Last Name', blank=True)
    institute = models.CharField(max_length=50, verbose_name='Institute', blank=True)

    def __str__(self):
        return self.email

class Reference(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default=uuid.uuid4,
        editable = False
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=30, verbose_name='Name', blank=True)
    email = models.EmailField(
        max_length = 255,
        verbose_name = 'email address',
    )

    letter = models.FileField(
        upload_to=directory_path_for_ref_letter,
        validators=[validate_file_extension], 
        blank=True
    )

    sent = models.BooleanField(default=False)
    received = models.BooleanField(default=False)



# Extending the base class that Django has for our customized User models.
class User(AbstractUser):
    # Removing the username field.
    #username = models.CharField(max_length=30, blank=True)
    #username = None
    
    id = models.UUIDField(
        primary_key = True,
        default=uuid.uuid4,
        editable = False
    )

    # Making the email field required and unique.
    email = models.EmailField(
        max_length = 255,
        verbose_name = 'email address',
        unique = True
    )
    
    first_name = models.CharField(max_length=30, verbose_name='First name', blank=True)
    last_name = models.CharField(max_length=30, verbose_name='Last name', blank=True)
    citizenship = models.CharField(max_length=30, verbose_name='Citizenship', blank=True)
    current_institute = models.CharField(max_length=50, verbose_name='Current institute', blank=True)
    address = models.CharField(max_length=100, verbose_name='Address', blank=True)
    city = models.CharField(max_length=30,  verbose_name='City', blank=True)
    province = models.CharField(max_length=30, verbose_name='Province', blank=True)
    postal = models.CharField(max_length=30, verbose_name='Zip/Postal', blank=True)
    country = models.CharField(max_length=30, verbose_name='Country', blank=True)
    phd_institute = models.CharField(max_length=50, verbose_name='PhD institute', blank=True)
    phd_year = models.CharField(max_length=50, verbose_name='Phd year', blank=True)
    research_interests = models.CharField(max_length=100, verbose_name='Research interests', blank=True)

    resume = models.FileField(
        upload_to=user_directory_path, 
        validators=[validate_file_extension], 
        blank=True,
    )

    research_statement = models.FileField(
        upload_to=user_directory_path, 
        validators=[validate_file_extension], 
        blank=True,
    )

    publication = models.FileField(
        upload_to=user_directory_path, 
        validators=[validate_file_extension], 
        blank=True,
    )

    sponsor_1 = models.ForeignKey(
        Sponsor,
        null=True,
        on_delete = models.SET_NULL,
        related_name='sponsor_1'
    )

    sponsor_2 = models.ForeignKey(
        Sponsor,
        null=True,
        on_delete = models.SET_NULL,
        blank=True,
        related_name='sponsor_2'
    )

    ref_1 = models.ForeignKey(
        Reference,
        null=True,
        on_delete = models.SET_NULL,
        related_name='ref_1'
    )

    ref_2 = models.ForeignKey(
        Reference,
        null=True,
        on_delete = models.SET_NULL,
        related_name='ref_2'
    )

    ref_3 = models.ForeignKey(
        Reference,
        null=True,
        on_delete = models.SET_NULL,
        related_name='ref_3'
    )


    #date_of_birth = models.DateField(default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    # Assigning the new Manager to the User model.
    objects = UserManager()
    
    # Telling Django that we are going to use the email field as the USERNAME_FIELD.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []#'first_name', 'last_name', 'citizenship', 'address', 'city', 'province', 'postal', 'country']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

#class Files(models.Model):
#    users = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
#    resume = models.FileField(
#        upload_to=user_directory_path,
#        validators=[validate_file_extension],
#    )

#def create_profile(sender, **kwargs):
#    if kwargs['created']:
#        user_profile = User.objects.create(email=kwargs['instance'])

#post_save.connect(create_profile, sender=User)
