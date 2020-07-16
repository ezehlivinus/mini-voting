from django.urls import path

from .views import RegistrationView, check_result, polling_unit, CreateVote, upload_students


urlpatterns = [
    path('polling-unit/', polling_unit, name='polling_unit'),
    path('register/', RegistrationView, name='register'),
    path('votes/', CreateVote, name='vote'),
    path('results/', check_result, name='result'),
    path('upload-voters/', upload_students, name='upload'),
]

