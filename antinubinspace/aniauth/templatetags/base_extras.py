from django import template

register = template.Library()

@register.simple_tag
def navactive(request, cat):
    if request.path.split("/")[1] == cat:
        return " class='active'"
    return ""