from django.http import HttpResponse
from django.views import View
from .tasks import hello

class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')


# CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine whether broker connection retries are made during startup in Celery 6.0 and above.
# If you wish to retain the existing behavior for retrying connections on startup, you should set broker_connection_retry_on_startup to True
