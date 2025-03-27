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
def to_jalali(value, format_string="Y/m/d H:i"):
    print(f"Input value: {value}, type: {type(value)}")  # دیباگ: چاپ مقدار ورودی
    try:
        # تبدیل تاریخ میلادی به شمسی
        jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
        # فرمت کردن تاریخ شمسی
        result = jalali_date.strftime(format_string)
        print(f"Converted to Jalali: {result}")  # دیباگ: چاپ نتیجه
        return result
    except (ValueError, TypeError) as e:
        print(f"Error in to_jalali: {e}")  # دیباگ: چاپ خطا
        return value