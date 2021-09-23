from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from .timestamp import TimeStamp


class SoftDeletionQuerySet(QuerySet):
    def delete(self, user=None):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now(), deleted_by=user)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(TimeStamp):
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_%(class)ss'
    )
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True
        ordering = ['id']

    def save(self, *args, **kwargs):
        user = kwargs.get('user', None)
        if user:
            if self.pk:
                self.updated_by = user
            else:
                self.created_by = user
                self.updated_by = user
            del kwargs['user']
        super(SoftDeletionModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = kwargs.get('user', None)
        if user:
            self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        user = kwargs.get('user', None)
        if user:
            self.updated_at = user
            self.updated_at = timezone.now()
        self.deleted_by = None
        self.deleted_at = None
        self.save()