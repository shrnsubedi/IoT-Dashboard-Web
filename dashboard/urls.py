from django.urls import path

from dashboard.views import DashboardDataAPI, DashboardDataView, PreferencesView

urlpatterns = [
    path("", DashboardDataView.as_view(), name="dashboard-landing_page"),
    path(
        "get_dashboard_data/",
        DashboardDataAPI.as_view(),
        name="dashboard-latest-readings",
    ),
    path("preferences/", PreferencesView.as_view(), name="preferences"),
]
