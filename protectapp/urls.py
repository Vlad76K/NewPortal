from django.urls import path, include
from .views import IndexView

urlpatterns = [
    # path('news/', include('newsportalapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('', IndexView.as_view()),
    # path('accounts/', include('protectapp.urls'))
]