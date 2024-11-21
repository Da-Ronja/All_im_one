from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _('Password must contain at least one uppercase letter.'), 
                code='password_no_upper'
            )
        
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _('Password must contain at least one digit.'), 
                code='password_no_digit'
            )
    
    def get_help_text(self):
        return _(
            'Your password must contain at least one uppercase letter and one digit.'
        )
