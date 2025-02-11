from django.contrib import admin
from .models import (
    Workspace, Team, Worker, Project, Sprint, Tag, 
    Bug, BugAttachment, ActivityLog, Notification, TimeTracking
)

# -------------------- Workspace Admin -------------------- #
@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


# -------------------- Team Admin -------------------- #
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace', 'created_at')
    search_fields = ('name', 'workspace__name')
    ordering = ('-created_at',)


# -------------------- Worker Admin -------------------- #
@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role', 'joined_at')
    list_filter = ('role', 'team')
    search_fields = ('user__username', 'team__name')


# -------------------- Project Admin -------------------- #
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace', 'assigned_team', 'created_at')
    list_filter = ('workspace', 'assigned_team')
    search_fields = ('name', 'workspace__name', 'assigned_team__name')
    ordering = ('-created_at',)


# -------------------- Sprint Admin -------------------- #
@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'project')
    search_fields = ('name', 'project__name')


# -------------------- Tag Admin -------------------- #
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -------------------- Bug Admin -------------------- #
@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'severity', 'priority', 'assigned_team', 'assigned_worker', 'created_at')
    list_filter = ('status', 'severity', 'priority', 'project', 'assigned_team')
    search_fields = ('title', 'description', 'project__name', 'assigned_worker__user__username')
    ordering = ('-created_at',)


# -------------------- BugAttachment Admin -------------------- #
@admin.register(BugAttachment)
class BugAttachmentAdmin(admin.ModelAdmin):
    list_display = ('bug', 'file', 'uploaded_at')
    search_fields = ('bug__title',)
    ordering = ('-uploaded_at',)


# -------------------- Activity Log Admin -------------------- #
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'project', 'bug', 'worker', 'created_at')
    list_filter = ('project', 'bug', 'worker')
    search_fields = ('message', 'project__name', 'bug__title', 'worker__user__username')
    ordering = ('-created_at',)


# -------------------- Notification Admin -------------------- #
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)


# -------------------- Time Tracking Admin -------------------- #
@admin.register(TimeTracking)
class TimeTrackingAdmin(admin.ModelAdmin):
    list_display = ('worker', 'bug', 'time_spent')
    list_filter = ('worker', 'bug')
    search_fields = ('worker__user__username', 'bug__title')

