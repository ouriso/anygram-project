from django import template
register = template.Library()


@register.filter 
def input_type(field_name):
    search = ['password', 'password1', 'password2']
    if field_name in search:
        return 'password'
    return 'text'
