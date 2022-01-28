from django import template

register = template.Library()

@register.simple_tag
def preview_bullet_list(bullet_list) -> list:
    """
    Returns a preview of the bullets in a lists for the general list view.
    """
    bullet_list = list(bullet_list)
    if len(bullet_list) <= 3:
        return bullet_list
    preview_list = bullet_list[:2]
    preview_list.append(f'And {len(bullet_list) - 2} bullets more...')
    return preview_list

@register.simple_tag(takes_context=True)
def is_empty_for_user(context, list_list):
    user_list_list = [list for list in list_list if list.author == context['user']]
    return len(user_list_list) == 0