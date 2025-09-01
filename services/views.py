from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer

class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_serializer_context(self):
        return {"request": self.request}
