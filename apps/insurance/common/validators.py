from django.core.exceptions import ValidationError

def mobile_char_check(mobile):
    if mobile.isnumeric() == False or len(mobile) != 10:
        raise ValidationError('Wrong phone number!')

