from django.db import models
from datetime import timedelta
from Auth.models import User

# --------------------------- 1️⃣ Workspace, Teams & Workers --------------------------- #
class Workspace(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="workers")
    role = models.CharField(max_length=50, choices=[("developer", "Developer"), ("tester", "Tester")], default="developer")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# --------------------------- 2️⃣ Project & Sprint Management --------------------------- #
class Project(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    github_repo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sprints")
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

# --------------------------- 3️⃣ Bug Tracking --------------------------- #
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Bug(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bugs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    tags = models.ManyToManyField(Tag, blank=True)
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="bugs")
    assigned_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="bugs")
    github_issue_url = models.URLField(blank=True, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="bugs")
    dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="blocked_by")
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reported_bugs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.project.name})"
    
    

# --------------------------- 4️⃣ Bug Attachments --------------------------- #
class BugAttachment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="bug_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)



# --------------------------- 5️⃣ Activity Logs & Notifications --------------------------- #
class ActivityLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="activity_logs")
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="activity_logs", null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.created_at}"
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"
    


# --------------------------- 6️⃣ Time Tracking --------------------------- #
class TimeTracking(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="time_tracking")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="time_spent")
    time_spent = models.DurationField(default=timedelta())

    def __str__(self):
        return f"{self.worker.user.username} - {self.bug.title}: {self.time_spent}"
    


# --------------------------- 7️⃣ Workflow Automation --------------------------- #
def auto_close_resolved_bugs(sender, instance, **kwargs):
    """ Automatically close resolved bugs after 7 days. """
    if instance.status == "resolved":
        instance.resolved_at = instance.updated_at + timedelta(days=7)

models.signals.pre_save.connect(auto_close_resolved_bugs, sender=Bug)
