
import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

now = dt.datetime.now()


def validate_title_year(value):
    if value <= 0 or value > now.year:
        raise ValidationError(
            _('%(value)s is not the correct year'),
            params={'value': value},
        )
