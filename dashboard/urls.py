from django.urls import path
from dashboard.views import DashboardDataView, DashboardDataAPI

urlpatterns = [
    path("", DashboardDataView.as_view(), name="dashboard-landing_page"),
    path(
        "get_dashboard_data/",
        DashboardDataAPI.as_view(),
        name="dashboard-latest-readings",
    ),
]
