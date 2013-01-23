from django.template import Library
from urlobject import URLObject
register = Library()
from lreviews.models import singlereviews

def query_LB_user(url, project,LB, user):
    rev = singlereviews.objects.filter(project=project,object_LB=LB,reviewer=user)
    return rev.count


register.filter('query_LB_user', query_LB_user)
