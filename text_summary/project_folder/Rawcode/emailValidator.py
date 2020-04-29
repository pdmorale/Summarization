from validate_email import validate_email
def emailValidator(account):
    is_valid = validate_email(account)
    return is_valid