from django.core.exceptions import ValidationError


'''Note that full_clean() will not be called automatically when you call your model’s save() method.
You’ll need to call it manually when you want to run one-step model validation for your own manually created models.
Example:

from django.core.exceptions import ValidationError
try:
    article.full_clean()
except ValidationError as e:
    # Do something based on the errors contained in e.message_dict.
    # Display them to a user, or handle them programmatically.
    pass'''