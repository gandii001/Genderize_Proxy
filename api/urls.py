from django.urls import path
from . views import classify_data 


urlpatterns = [
    path("api/classify", classify_data.as_view())
]