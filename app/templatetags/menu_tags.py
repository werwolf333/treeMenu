from django import template
from ..models import MenuItem
from django.db.models import Subquery, Q

register = template.Library()


def get_active_menu_item(request, top_level_items):
    for item in top_level_items:
        if request.path == item.link:
            return item


def render_menu_items(top_level_items, current_active_item):
    rendered_menu_items = []
    if current_active_item is None:
        hide_next = True
    else:
        hide_next = False

    for item in top_level_items:
        if hide_next:
            rendered_item = render_hidden_item(item)
        else:
            if is_menu_item_active(item, current_active_item):
                if item == current_active_item:
                    rendered_item = render_active_item(item)
                else:
                    rendered_item = render_partially_visible_item(item, current_active_item)
                hide_next = True
            else:
                rendered_item = render_menu_item(item)

        rendered_menu_items.append(rendered_item)

    return rendered_menu_items


def is_menu_item_active(menu_item, current_active_item):
    def find_item(item, target):
        if item == target:
            return True
        for child in item.children.all():
            if find_item(child, target):
                return True
        return False
    return find_item(menu_item, current_active_item)


def render_partially_visible_item(menu_item, current_active_item):
    rendered_child_items = []
    children = menu_item.children.all()

    hide_next = False
    for child in children:
        if hide_next:
            rendered_child = render_hidden_item(child)
        else:
            if is_menu_item_active(child, current_active_item):
                if child == current_active_item:
                    rendered_child = render_active_item(child)
                else:
                    rendered_child = render_menu_item(child)
                hide_next = True
            else:
                rendered_child = render_menu_item(child)

        rendered_child_items.append(rendered_child)

    return {
        'name': menu_item.name,
        'link': menu_item.link,
        'label': menu_item.label,
        'children': rendered_child_items
    }


def render_active_item(menu_item):
    rendered_child_items = []
    children = menu_item.children.all()
    for child in children:
        rendered_child_items.append({
            'name': child.name,
            'link': child.link,
            'label': child.label,
            'children': []
        })
    return {
        'name': menu_item.name,
        'link': menu_item.link,
        'label': menu_item.label,
        'children': rendered_child_items
    }


def render_menu_item(menu_item):
    rendered_child_items = []
    children = menu_item.children.all()
    for child in children:
        rendered_child = render_menu_item(child)
        rendered_child_items.append(rendered_child)
    return {
        'name': menu_item.name,
        'link': menu_item.link,
        'label': menu_item.label,
        'children': rendered_child_items
    }


def render_hidden_item(menu_item):
    return {
        'name': menu_item.name,
        'link': menu_item.link,
        'label': menu_item.label,
        'children': []
    }


@register.inclusion_tag('menu.html')
def draw_menu(request, menu_name):
    if request.path.endswith('/favicon.ico/'):
        return {}

    all_menu_items = MenuItem.objects.filter(name=menu_name).select_related('parent').prefetch_related('children')
    top_level_items = all_menu_items.filter(parent__isnull=True)

    current_active_item = get_active_menu_item(request, all_menu_items)
    rendered_menu_items = render_menu_items(top_level_items, current_active_item)

    return {
        'menu_items': rendered_menu_items
    }


@register.simple_tag
def render_menu(menu_items):
    output = '<ul>'
    for menu_item in menu_items:
        output += '<li>'
        link = menu_item['link']
        label = menu_item['label']
        output += f'<a href="{link}">{label}</a>'
        if menu_item['children']:
            output += render_menu(menu_item['children'])
        output += '</li>'
    output += '</ul>'
    return output
