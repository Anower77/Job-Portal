from django import template
from jobapp.models import Applicant

register = template.Library()

@register.simple_tag
def get_total_applicant(job):
    if job:
        return Applicant.objects.filter(job=job).count()
    return 0 