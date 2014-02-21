# coding: utf-8
from django.contrib.auth.models import Permission


def get_permission_codename(cls, field):
    return 'change_' + cls.__name__.lower() + '_' + field.lower()


def get_guarded_fields(self, request):
    guarded_fields = []
    for field, (permission_codename, permission_name) in self.model.fieldguard.items():
        if not request.user.has_perm(self.__module__.split('.')[0] + '.' + permission_codename):
            guarded_fields.append(field)

    return guarded_fields


class guard(object):
    """ A decorator to add some permissions to something """

    # Parse args
    def __init__(self, *args):
        self.explicit_fields = args

    # Decorate
    def __call__(self, cls):
        # Adds permissions for fields to cls._meta and fieldguard array to the class
        fields = self.explicit_fields or [field.name for field in cls._meta.fields]
        cls.fieldguard = {}

        for field in fields:
            permission_codename = get_permission_codename(cls, field)
            permission_name = 'Can change ' + cls.__name__ + '[' + field + ']'

            cls._meta.permissions.append(
                (permission_codename, permission_name)
            )
            cls.fieldguard[field] = (permission_codename, permission_name)

        return cls


class enforce(object):
    """ Enforce the permissions set by guard for some ModelAdmin """

    def __call__(self, cls):
        cls.get_guarded_fields = get_guarded_fields

        def get_readonly_fields(self, request, obj=None):
            readonly_fields = super(self.__class__, self).get_readonly_fields(request, obj)
            guarded_fields = self.get_guarded_fields(request)
            return set(self.readonly_fields).union(set(guarded_fields))
        cls.get_readonly_fields = get_readonly_fields

        def get_prepopulated_fields(self, request, obj=None):
            prepopulated_fields = super(self.__class__, self).get_prepopulated_fields(request, obj)
            for guarded_field in self.get_guarded_fields(request):
                # If guarded field is prepopulated field
                if guarded_field in prepopulated_fields:
                    del(prepopulated_fields[guarded_field])
                # If guarded field is in prepopulated field's dependencies
                for key in prepopulated_fields.keys():
                    if guarded_field in prepopulated_fields[key]:
                        del(prepopulated_fields[key])
            return prepopulated_fields
        cls.get_prepopulated_fields = get_prepopulated_fields

        return cls
