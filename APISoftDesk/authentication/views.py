from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.serializers import UserCreation as s_UserCreation


class UserCreation(ModelViewSet):

    serializer_class = s_UserCreation

    def get_permissions(self):
        permission_classes = []
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Get list fo every User in DB
        :return: All DB  ->  User(AbstractUser)
        """
        return User.objects.all()
