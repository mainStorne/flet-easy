from flet_easy.forms.fields import Fieldsy


def required(obj: Fieldsy):
    """Execute __required__ dunder method of Fieldsy object"""
    obj.__required__()
