from django.urls import path
from . import views

app_name = 'results'
urlpatterns = [
    path('', views.AllureResultListView.as_view()),
    path('<int:id>', views.AllureResultDetailView.as_view()),
]

