from django.contrib import admin
from authentication.models import User
from project.models import Project, Issue, Comment, Contributors

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributors)
