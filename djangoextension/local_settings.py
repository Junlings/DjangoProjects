
""" This is the commonly used settings """

# settings for the auth profile module
AUTH_PROFILE_MODULE = 'accounts.UserProfile'


# settings for the django-registration
LOGIN_URL = 'accounts/login/'
REGISTER_URL = 'accounts/'
LOGIN_REDIRECT_URL = '/'

LOGIN_EXEMPT_URLS = (
    r'^$',
    r'^favicon\.ico$',
    r'^about\.html$',
    r'^legal/', # allow the entire /legal/* subsection
    r'^accounts/login/$',
    r'^accounts/register/$',
    r'^accounts/register/complete/$',
    r'^accounts/register/closed/$',
    r'^accounts/activate/complete/',
    r'^accounts/activate/(?P<activation_key>\w+)/$',
    r'^password/reset/$',
    r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^password/reset/complete/$',
    r'^password/reset/done/$',
)

ACCOUNT_ACTIVATION_DAYS = 7  # django registration


# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.fprimes.com'
EMAIL_HOST_USER = 'customerservice@fprimes.com'
EMAIL_HOST_PASSWORD = 'xiajun201080'
EMAIL_PORT = 26
DEFAULT_FROM_EMAIL = 'customerservice@fprimes.com'
