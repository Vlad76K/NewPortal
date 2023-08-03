from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    # path('accounts/', include('allauth.urls')),
    # path('accounts/', include('protectapp.urls'))
]