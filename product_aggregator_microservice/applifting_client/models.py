from django.db import models


class AppliftingToken(models.Model):
    token = models.CharField()
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ["-created_at"]
