from django.db import models

class Website(models.Model):
    id = models.CharField(max_length=20, primary_key=True, db_index=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.id})"


class PageView(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, blank=True, null=True)
    hash_id = models.CharField(max_length=64)
    path = models.CharField(max_length=2048)
    referrer = models.CharField(max_length=2048, null=True, blank=True)
    device = models.CharField(max_length=100)
    browser = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pageviews'
        indexes = [
            models.Index(fields=['website', 'timestamp']),
            models.Index(fields=['website', 'timestamp', 'path']),
            models.Index(fields=['website', 'timestamp', 'referrer']),
            models.Index(fields=['website', 'timestamp', 'country']),
            models.Index(fields=['website', 'timestamp', 'device']),
            models.Index(fields=['website', 'timestamp', 'browser']),
            models.Index(fields=['hash_id', 'path', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.path} - {self.timestamp}"


class Event(models.Model):
    """A user-triggered event (click, download, submit, custom JS action).

    Mirrors PageView's identity and dimension columns on purpose so the
    visitor privacy model (salted daily `hash_id`, no cookies, no PII) is
    inherited verbatim and dashboard queries can run the same WHERE clause
    against `events` as against `pageviews`.
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, blank=True, null=True)
    hash_id = models.CharField(max_length=64)
    name = models.CharField(max_length=255)  # e.g. 'download:estonia-report.pdf' — site-author-chosen
    path = models.CharField(max_length=2048)
    referrer = models.CharField(max_length=2048, null=True, blank=True)
    device = models.CharField(max_length=100)
    browser = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'
        indexes = [
            models.Index(fields=['website', 'timestamp', 'name']),
            models.Index(fields=['website', 'timestamp', 'path']),
            models.Index(fields=['website', 'timestamp', 'referrer']),
            models.Index(fields=['hash_id', 'name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.name} - {self.timestamp}"
