"""
core/templatetags/ui_tags.py
Custom template tags for reusable UI components.
"""

from django import template

register = template.Library()


@register.inclusion_tag('partials/action_buttons.html')
def action_buttons(edit_url, delete_url,
                   edit_perm=False, delete_perm=False,
                   confirm_msg='Are you sure?'):
    """
    Render a row of View / Edit / Delete action buttons.

    Usage in templates:
        {% load ui_tags %}
        {% action_buttons
            edit_url=edit_url_variable
            delete_url=delete_url_variable
            edit_perm=perms.app.change_model
            delete_perm=perms.app.delete_model
            confirm_msg="Delete this item?"
        %}

    Note: edit_url and delete_url must be pre-built with {% url %} … as varname
    before calling this tag.
    """
    return {
        'edit_url':    edit_url,
        'delete_url':  delete_url,
        'edit_perm':   edit_perm,
        'delete_perm': delete_perm,
        'confirm_msg': confirm_msg,
    }
