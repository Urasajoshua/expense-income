from rest_framework import generics ,status
from . import serializers
from . models import Expense
from rest_framework import permissions
from .permission import IsOwner

class ExpenseList(generics.ListCreateAPIView):
    serializer_class=serializers.ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    

class ExpenseDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=serializers.ExpenseSerializer
    queryset=Expense.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsOwner,)
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    
    
    
    
