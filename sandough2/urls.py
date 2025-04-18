from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core.views import dashboard_view  # فقط dashboard_view رو وارد می‌کنیم

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('deposit/', include('deposit.urls')),
    path('withdrawal/', include('withdrawal.urls')),
    path('loan/', include('loan.urls')),
    path('reports/', include('reports.urls')),
    path('balance/', include('balance.urls')),
    path('customer/', include('customer.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', lambda request: redirect('login'), name='root'),
]

# اضافه کردن تنظیمات برای فایل‌های رسانه‌ای (مثل id_copy توی مدل Customer)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)