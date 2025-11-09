#studio/model.py
from django.db import models

class StudioTask(models.Model):
    file = models.FileField(upload_to="uploads/")
    prompt = models.TextField()
    result_file = models.FileField(upload_to="results/", null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.id} - {self.status}"
