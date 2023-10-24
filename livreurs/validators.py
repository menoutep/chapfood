
from datetime import timezone
from datetime import date
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
    raise ValidationError(("Le mot de passe : %(value)s doit avoir au moins 8 charactères"),code="too_short_password",params={"value":password})

  # Check if the password contains at least one capital letter.
  if not any(char.isupper() for char in password):
    raise ValidationError(("Le mot de passe : %(value)s doit avoir au moins une lettre majuscule."),code="no_capital_letter",params={"value":password})

  # Check if the password contains at least one number.
  if not any(char.isdigit() for char in password):
    raise ValidationError(("Le mot de passe : %(value)s doit avoir au moins un chiffre"),code="no_digit_character",params={"value":password})

  # The password meets all the criteria.
  return True

def mail_is_unique(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email déjà existant: %(value)s", code="email_not_unique", params={"value": email})
    else :
        return True
  
def username_is_unique(username):
  user = User.objects.filter(username=username).exists()
  if user :
    raise ValidationError(("Username déja existant: %(value)s"),code="username_not_unique",params={"value":username})
  else :
    return True


def validate_age(date_of_birth):
    age = date.today().year - date_of_birth.year - ((date.today().month, date.today().day) < (date_of_birth.month, date_of_birth.day))
    if age < 18:
        raise ValidationError("L'âge doit être d'au moins 18 ans.")