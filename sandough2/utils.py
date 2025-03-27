from django_jalali.templatetags.jalali_tags import to_jalali as dj_to_jalali

def to_jalali(gregorian_date):
    return dj_to_jalali(gregorian_date)