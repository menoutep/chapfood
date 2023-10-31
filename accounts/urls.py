from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetCompleteView,PasswordResetDoneView,PasswordResetConfirmView
from .forms import PasswordResetForm,PasswordChangeForm,SetPasswordForm
app_name='accounts'
urlpatterns = [
    path('signup/',views.SignUpView, name="signup"),
    path('login/',views.custom_login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', PasswordResetView.as_view(template_name='accounts/password_reset.html',success_url=reverse_lazy('accounts:password_reset_done'),form_class=PasswordResetForm,email_template_name='accounts/password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html',form_class=PasswordChangeForm,success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    path('forget_password/', PasswordResetView.as_view(template_name='accounts/password_reset.html',success_url=reverse_lazy('accounts:forget_password_reset_done'),form_class=PasswordResetForm,email_template_name='accounts/forget_password_reset_email.html'), name='forget_password_reset'),
    path('forget_password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name="forget_password_reset_done"),
    path('forget_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html',success_url=reverse_lazy('accounts:forget_password_reset_complete'),form_class=SetPasswordForm), name='forget_password_reset_confirm'),
    path('forget_reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='forget_password_reset_complete'),
]