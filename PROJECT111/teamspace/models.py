from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=50)
    birthdate = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    introduction = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserSkills(models.Model):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    PROFICIENCY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)

    class Meta:
        unique_together = ('user', 'skill')


class Projects(models.Model):
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    goal = models.TextField(null=True, blank=True)
    tech_stack = models.TextField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Teams(models.Model):
    project = models.OneToOneField(Projects, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class TeamMembers(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')


class MatchScores(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    score = models.FloatField()
    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')


class Evaluations(models.Model):
    evaluator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='given_evaluations')
    evaluatee = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_evaluations')
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField(null=True, blank=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('evaluator', 'evaluatee', 'team')


class Portfolios(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
