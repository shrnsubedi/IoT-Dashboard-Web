from django.urls import path
from dashboard.views import LandingPage
urlpatterns = [
    path("", LandingPage.as_view(), name="dashboard-landing_page")
]
