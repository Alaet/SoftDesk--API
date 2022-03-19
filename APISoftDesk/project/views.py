from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from project.models import Project, Contributors, Issue, Comment
from project.permissions import IsAdmin, IsOwner, IsContributor
from project.serializers import CommentListSerializer, \
    ProjectDetailSerializer, IssueDetailSerializer, \
    ProjectListSerializer, ContributorsListSerializer,\
    CommentDetailSerializer, IssueListSerializer


class ProjectViewSet(ModelViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            permission_classes = [
                IsContributor,
                IsAuthenticated,
            ]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]
        elif self.request.method == "POST":
            permission_classes = [
                IsContributor,
                IsAuthenticated,
                IsAdmin,
            ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create' or self.action == 'update':
            return ProjectDetailSerializer
        return ProjectListSerializer

    def get_queryset(self):
        projects = Contributors.objects.filter(user_id=self.request.user.id).values_list('project_id', flat=True)
        if not projects:
            raise ValidationError("Vous n'avez pas de projet en cours")
        return Project.objects.filter(id__in=projects)

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save()
        Contributors.objects.create(project_id=instance, user_id=user)


class IssueViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create' or self.action == 'update':
            return IssueDetailSerializer
        return IssueListSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            permission_classes = [
                IsContributor,
                IsAuthenticated,
            ]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        pk_project = self.kwargs.get('id_project')
        issues = Issue.objects.filter(project_id=pk_project)
        if not issues:
            raise ValidationError("Le projet n'a pas de problème")
        return issues

    def perform_create(self, serializer):
        user = self.request.user
        pk_project = self.kwargs.get('id_project')
        project = get_object_or_404(Project, pk=pk_project)
        serializer.save(project_id=project, author_user_id=user, assignee_user_id=user)


class CommentViewSet(ModelViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            permission_classes = [
                IsContributor,
                IsAuthenticated,
            ]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create' or self.action == 'update':
            return CommentDetailSerializer
        return CommentListSerializer

    def get_queryset(self):
        pk_issue = self.kwargs.get('id_issue')
        comment = Comment.objects.filter(issue_id=pk_issue)
        if not comment:
            raise ValidationError("Le commentaire au problème que vous cherchez n'existe pas.")
        return comment

    def perform_create(self, serializer):
        user = self.request.user
        pk_issue = self.kwargs.get('id_issue')
        issue = get_object_or_404(Issue, pk=pk_issue)
        serializer.save(issue_id=issue, author_user_id=user)


class ContributorsListViewSet(ModelViewSet):
    serializer_class = ContributorsListSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            permission_classes = [
                IsContributor,
                IsAuthenticated,
            ]
        elif self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [
                IsContributor,
                IsAuthenticated,
                IsAdmin,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        pk_project = self.kwargs.get('id_project')
        project_contributors = Contributors.objects.filter(project_id=pk_project)
        return project_contributors

    def perform_create(self, serializer):
        pk_project = self.kwargs.get('id_project')
        project = get_object_or_404(Project, pk=pk_project)
        serializer.save(project_id=project)
