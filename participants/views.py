from rest_framework import permissions, viewsets

from .models import Registration
from .serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


#| Método | Endpoint                | Acesso      |
#| ------ | ----------------------- | ----------- |
#| GET    | /api/registrations/   | Público     |
#| GET    | /api/registrations/1/ | Público     |
#| POST   | /api/registrations/   | Autenticado |
#| PUT    | /api/registrations/1/ | Autenticado |
#| PATCH  | /api/registrations/1/ | Autenticado |
#| DELETE | /api/registrations/1/ | Autenticado |
