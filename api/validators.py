import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

current_year = dt.datetime.now().year


def validate_title_year(value):
    """check of the year.
       The year cannot be less than the year of the creation of the Earth
       and more than the current + 50 years (otherwise it will be difficult
       to analyze our data due to the many incorrect values)
    """
    if value > current_year + 50 or value < -45000004000:
        raise ValidationError(
            _('%(value)s is not the correct year'),
            params={'value': value},
        )
