from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.utils.translation import ugettext_lazy as _
from accounts.models import Account

#----------------- SIGN UP VALIDATIONS -----------------
# Password validation
def validatePassword(password):
    if len(password) < 6:
        raise ValidationError(
            _('Password is too short'),
        )

# E-mail validation
def validateEmail(email):
    # Proper Check
    try:
        validate_email(email)
    except ValidationError as e:
        raise ValidationError(
            _('"%(email)s" is not a valid email.'), params={'email': email},
        )
    # Already exists check
    qs = User.objects.filter(email=email)
    if qs.exists():
        raise ValidationError(
            _("'%(email)s' is already registered"), params={'email':email}
        )
# Name validation
def validateName(name):
    if not re.compile("^[A-Za-z .-]+$").match(name):
        raise ValidationError(
            _('"%(name)s" contains invalid character.'), params={'name': name},
        )
