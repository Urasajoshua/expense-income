from django.urls import path
from . import views


urlpatterns = [
    path('',views.ExpenseList.as_view(),name='expense'),
    path('<int:id>',views.ExpenseDetailsApiView.as_view(),name='expense_id')
]