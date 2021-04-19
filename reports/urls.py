from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.AllureReportListView.as_view()),
    path('<int:id>', views.AllureReportDetailView.as_view()),
]

