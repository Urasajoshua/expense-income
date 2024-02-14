from django.urls import path
from . import views


urlpatterns = [
    path('',views.IncomeList.as_view(),name='IncomeList'),
    path('<int:id>',views.IncomeDetailsApiView.as_view(),name='expense_id')
]