from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from project.models import Contributors, Issue, Comment, Project


class IsAdmin(BasePermission):
    """
    Check for user attribute is_staff and return value
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsOwner(BasePermission):
    """
    Check if request.user is creator of an object, based on obj type
    """
    def has_object_permission(self, request, view, obj):
        """
        Grant permissions base on type object in params and request user relation to obj
        :param request:
        :param view:
        :param obj:
        :return: bool
        """
        # if isinstance(obj, Issue) or isinstance()
        if type(obj) == Issue or type(obj) == Comment:
            if request.user.id == obj.author_user_id.id:
                return True
            raise ValidationError("Seul l'auteur %s peut le modifier ou le supprimer" % obj.author_user_id)
        elif type(obj) == Project:
            owner = Contributors.objects.filter(project_id=obj.id).values_list('user_id', flat=True)
            if request.user.id == owner[0]:
                return True
            raise ValidationError("Seul l'auteur %s peut le modifier" % owner[0])


class IsContributor(BasePermission):
    """
    Check if request.user is a contributor of a project
    """
    def has_permission(self, request, view):
        if request.resolver_match.kwargs:
            try:
                pk_project = int(request.resolver_match.kwargs["id_project"])
            except KeyError:
                pk_project = int(request.resolver_match.kwargs["pk"])
            contributions = Contributors.objects.filter(project_id=pk_project).values_list('user_id', flat=True)
            if request.user.id in contributions:
                return True
            else:
                return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if type(obj) == Issue:
            contrib = Contributors.objects.filter(project_id=obj.project_id.id).values_list('user_id', flat=True)
            if request.user.id in contrib:
                return True
        elif type(obj) == Project:
            contrib = Contributors.objects.filter(project_id=obj.id).values_list('user_id', flat=True)
            if request.user.id in contrib:
                return True
        elif type(obj) == Comment:
            issue = get_object_or_404(Issue, pk=obj.issue_id.id)
            contrib = Contributors.objects.filter(project_id=issue.project_id).values_list('user_id', flat=True)
            if request.user.id in contrib:
                return True
        elif type(obj) == Contributors:
            contrib = Contributors.objects.filter(project_id=obj.project_id.id).values_list('user_id', flat=True)
            if request.user.id == contrib[0]:
                return True
