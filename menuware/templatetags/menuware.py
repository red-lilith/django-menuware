from django import template
from django.conf import settings

from ..menu import generate_menu
from .. import defaults as defs
from ..utils import get_func


MENUS_NAME = ".menus.MENUWARE_MENU"
register = template.Library()


@register.simple_tag(takes_context=True)
def get_menu(context, menu_name):
    """
    Returns a consumable menu list for a given menu_name found in settings.py.
    Else it returns an empty list.
    """
    menu_list = get_menus_from_apps(menu_name)
    return generate_menu(context['request'], menu_list)


def get_menus_from_apps(name):
    installed_apps = getattr(settings, "INSTALLED_APPS", defs.MENU_NOT_FOUND)
    if installed_apps == defs.MENU_NOT_FOUND:
        return installed_apps

    menu_list = []
    for app in installed_apps:
        menu_dict = get_func(app + MENUS_NAME)
        if not menu_dict:
            continue
        menu_list += menu_dict.get(name, [])
    return menu_list