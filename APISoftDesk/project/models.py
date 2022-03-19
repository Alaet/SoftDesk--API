from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class Issue(models.Model):
    """
    Related to a Project by foreignKey, hold comment, can be assign to a user (default: author_uder_id)
    """
    TAG_CHOICES = (
        ('BUG', 'BUG'),
        ('UPD', 'AMELIORATION'),
        ('TASK', 'TÂCHE'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'FAIBLE'),
        ('MED', 'MOYENNE'),
        ('HIGH', 'ELEVEE'),
    )
    STATUS_CHOICES = (
        ('TODO', 'A FAIRE'),
        ('CURR', 'EN COURS'),
        ('DONE', 'TERMINE'),
    )
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1200)
    tag = models.CharField(max_length=50, choices=TAG_CHOICES, default='BUG')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='LOW')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='TODO')
    author_user_id = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="issues_author")
    assignee_user_id = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, null=True,
                                         related_name="issues_assignee", default=author_user_id)
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="issues", null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    Managed only by staff user, associated to Issue, filled with comments. Hold every issue and comment relative to
    a project. (TYPE_CHOICES)
    """
    TYPE_CHOICES = (
        ('BE', 'BACK-END'),
        ('FE', 'FRONT-END'),
        ('IOS', 'iOS'),
        ('AND', 'ANDROID'),
    )
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    contributor = models.ManyToManyField(USER_MODEL, through='Contributors', related_name='contributor')

    def __str__(self):
        return self.title


class Contributors(models.Model):
    """
    Object representing the relation between a user and a project
    """
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project_id', 'user_id')


class Comment(models.Model):
    """
    Comment made by a user related to an Issue (self related to a project)
    """
    description = models.CharField(max_length=1200)
    author_user_id = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
