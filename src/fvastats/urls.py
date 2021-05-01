from django.urls import path

from . import views as stats
from .serialtime import show_timeperminute

urlpatterns = [
    path("corebase_stats", stats.render_stats, name="index_stats"),
    path("durations_stats", stats.get_durations_stats, name="durations_stats"),
    path("get_total_stats", stats.get_total_stats, name="total_stats"),
    path("get_error_stats", stats.get_error_stats, name="error_stats"),
    path("get_size_stats", stats.get_size_stats, name="size_stats"),
    path("total_per_minute", show_timeperminute, name="total_per_minute"),
    path("show_summary", stats.show_summary, name="show_summary"),
]