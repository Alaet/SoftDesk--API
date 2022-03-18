from rest_framework.serializers import ModelSerializer


from project.models import Project, Contributors, Issue, Comment


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            "author_user_id": {'required': False},
            "issue_id": {'required': False},
        }


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag', 'priority']


class IssueDetailSerializer(ModelSerializer):

    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'author_user_id', 'assignee_user_id', 'tag', 'priority', 'status',
                  'comments']
        extra_kwargs = {
            "author_user_id": {"required": False},
            "tag": {"required": True},
            "priority": {"required": True},
            "status": {"required": True},
        }


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'type']


class ProjectDetailSerializer(ModelSerializer):

    issues = IssueListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ContributorsListSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['id', 'user_id']



