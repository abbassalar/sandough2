from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        # تبدیل به عدد صحیح
        value = int(float(value))
        # اضافه کردن جداکننده سه رقم
        return "{:,}".format(value)
    except (ValueError, TypeError):
        return value