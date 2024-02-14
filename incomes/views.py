from rest_framework import generics ,status
from . import serializers
from . models import Income
from rest_framework import permissions
from .persmission import IsOwner

class IncomeList(generics.ListCreateAPIView):
    serializer_class=serializers.IncomeSerializer
    queryset = Income.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    

class IncomeDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=serializers.IncomeSerializer
    queryset=Income.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsOwner,)
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    
    
    
    
