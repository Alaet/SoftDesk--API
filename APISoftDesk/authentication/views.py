from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import SignupPermissions
from authentication.serializers import UserCreation as s_UserCreation
from project.models import USER_MODEL


class UserCreation(ModelViewSet):

    serializer_class = s_UserCreation
    permission_classes = [IsAuthenticated, SignupPermissions]

    def get_queryset(self):
        """
        Get list fo every User in DB
        :return: All DB  ->  User(AbstractUser)
        """
        return USER_MODEL.objects.all()
