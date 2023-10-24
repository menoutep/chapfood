
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
def validate_password(password):
  """
  Validates a password according to the given criteria.

  Args:
    password (str): The password to validate.

  Returns:
    bool: True if the password is valid, False otherwise.
  """

  # Check if the password is at least 8 characters long.
  if len(password) < 8:
    return False

  # Check if the password contains at least one capital letter.
  if not any(char.isupper() for char in password):
    
    return False

  # Check if the password contains at least one number.
  if not any(char.isdigit() for char in password):
    return False

  # The password meets all the criteria.
  return True

def mail_is_unique(email):
  user_ = User.objects.get(email=email)
  if user_ : 
    raise ValidationError(("Email déja existant: %(value)s"),code="email_not_unique",params={"value": email})
    return False
  else :
    return True
  
def username_is_unique(username):
  user = User.objects.get(username=username)
  if user :
    raise ValidationError(("Username déja existant: %(value)s"),code="username_not_unique",params={"value":username})
    return False
  else :
    return True


