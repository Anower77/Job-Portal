from django import template
from jobapp.models import Applicant

register = template.Library()

@register.simple_tag
def is_job_already_applied(job, user):
    if user.is_authenticated:
        return Applicant.objects.filter(user=user, job=job).exists()
    return False 