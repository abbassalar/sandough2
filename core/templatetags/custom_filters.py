from django import template
import jdatetime

register = template.Library()

@register.filter
def format_price(value):
    try:
        value = int(float(value))
        return "{:,}".format(value)
    except (ValueError, TypeError):
        return value

@register.filter
def to_jalali(value, format_string="%Y/%m/%d %H:%M"):
    try:
        if not value:
            return "تاریخ نامعتبر"
        # تبدیل تاریخ میلادی به شمسی
        jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
        # فرمت کردن تاریخ شمسی با فرمت استاندارد پایتون
        return jalali_date.strftime(format_string)
    except (ValueError, TypeError) as e:
        return f"خطا در تبدیل تاریخ: {str(e)}"