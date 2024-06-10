# Custom User Model

## Building a custom user model in Django

Assuming `Python` and `pipen` are installed.

1. Creating new directory for the project and install Django with pipenv

```bash
mkdir custom_user_model
cd custom_user_model

pipenv install django
```

2. Create a new Django project

```bash
django-admin startproject main .
```
this will create a new Django project in the current directory.  

3. Create a new Django app

```bash
python manage.py startapp account
```

4. Add the app to the installed apps in the `main/settings.py` file

*Also adding the custom user model*

```python
...
AUTH_USER_MODEL = 'account.Account' # This is the custom user model we are creating

INSTALLED_APPS = [
	...
	'account',
]
...
```

5. Create a custom user model in the `account/models.py` file

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have a username")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
		)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


def get_profile_image_filepath(self, filename):
	return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
	return "profile_images/default.png"

class Account(AbstractBaseUser):

	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	prfile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email = models.BooleanField(default=True)

	objects = MyAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	def __str__(self):
		return self.username
	
	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/{self.pk}/'):]	

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

```

**Note**: *The images we refer to in the get_default_profile_image() function are not available yet. The set up will be done later in this tutorial* !!!

6. Making migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser

```bash
python manage.py createsuperuser
```

8. Run the server

```bash
python manage.py runserver
```

**Note:** *At this point, we can now login to the admin panel and see the custom user model we created with the fields we specified.*  

Next we will handle the authentication process with case-insensitive email and username.  


## Handling case-insensitive email and username

Here we creating a custom authentication backend module to handle the authentication process with case-insensitive email and username.  

1. Create a custom authentication backend in the `account/backends.py` file in the `account` app  

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):

	# Overriding the authenticate method
	def authenticate(self, request, username=None, password=None, **kwargs):
		
		UserModel = get_user_model() # Getting the user model defined in the settings.py file (AUTH_USER_MODEL..)

		if username is None:
			username = kwargs.get(UserModel.USERNAME_FIELD) # Getting the username field from models.py (USERNAME_FIELD..)
		try:
			case_insensitive_username_field = f'{UserModel.USERNAME_FIELD}__iexact'
			user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
		except UserModel.DoesNotExist:
			UserModel().set_password(password)

		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user
```

2. Add the custom authentication backend to the `main/settings.py` file

```python
# after the AUTH_USER_MODEL adding the custom authentication backend
AUTH_USER_MODEL = 'account.Account'
AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.AllowAllUsersModelBackend',
	'account.backends.CaseInsensitiveModelBackend',
]
```

*This will allow us to authenticate the user if the email or username is entered in any case*  

**NOTE**: We can use the following command to save the requirements of the project to a file  

```bash
pip freeze > requirements.txt
```

*This will save all the packages installed in the project to a file named `requirements.txt`*  
