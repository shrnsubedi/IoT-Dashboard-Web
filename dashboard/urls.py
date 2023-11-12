from django.urls import path
from dashboard.views import LandingPageView, LatestSensorDataView
urlpatterns = [
    path("", LandingPageView.as_view(), name="dashboard-landing_page"),
    path("get_latest_readings/", LatestSensorDataView.as_view(), name="dashboard-latest-readings")
]
