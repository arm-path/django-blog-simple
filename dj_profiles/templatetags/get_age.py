from datetime import datetime

from django import template

register = template.Library()


@register.filter()
def get_age(date_birth):
    date_now = datetime.now().date()
    age = int((date_now - date_birth).days / 365)
    if date_now.month > date_birth.month or (date_now.month == date_birth.month and date_now.day >= date_birth.day):
        age += 1
    return f'{age} лет'
