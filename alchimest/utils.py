from django.db.models import fields

def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name))
                    for f in obj._meta.fields
                    if not isinstance(f, fields.UUIDField) and
                       not f in obj._meta.parents.values()])
    return obj.__class__(**initial)