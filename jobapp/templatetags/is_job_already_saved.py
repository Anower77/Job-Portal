from django import template
from jobapp.models import BookmarkJob

register = template.Library()

@register.simple_tag
def is_job_already_saved(job, user):
    if user.is_authenticated:
        return BookmarkJob.objects.filter(user=user, job=job).exists()
    return False 