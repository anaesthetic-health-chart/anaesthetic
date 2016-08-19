"""
ffs.contrib.mold

Useful for easy template rendering
"""

import jinja2

__all__ = [
    'cast'
    ]

def cast(template, **context):
    """
    Render TEMPLATE using **CONTEXT.

    Assume TEMPLATE is a Jinja2 template.


    Arguments:
    - `template`: Path
    - `**context`: dict

    Return: unicode
    Exceptions: None
    """
    tpl = jinja2.Template(template.contents)
    return tpl.render(**context)

