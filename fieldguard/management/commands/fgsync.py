from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from fieldguard import get_permission_codename


class Command(BaseCommand):
    help = 'Update fieldguard per-field permissions in the database'

    def handle(self, *args, **kwargs):
        for model in models.loading.get_models():
            module_name = model.__module__.split('.')[0]
            model_name = model.__name__.lower()
            try:
                content_type = ContentType.objects.get(app_label=module_name, model=model_name)
            except ContentType.DoesNotExist:
                continue

            if hasattr(model, 'fieldguard'):
                for (permission_codename, permission_name) in model.fieldguard.values():
                    self.stdout.write('Creating field permission ' + permission_name + ' for model ' + model_name + '... ', ending='')
                    permission, created = Permission.objects.get_or_create(
                        codename=permission_codename,
                        name=permission_name,
                        content_type=content_type,
                    )
                    if created:
                        self.stdout.write('ok')
                    else:
                        self.stdout.write('already exists')

            for field in model._meta.fields:
                field_name = field.name
                if not hasattr(model, 'fieldguard') or not field_name in model.fieldguard:
                    try:
                        permission = Permission.objects.get(
                            codename=get_permission_codename(model, field_name),
                            content_type=content_type
                        )
                        self.stdout.write('Deleted stale field permission ' + permission.name)
                        permission.delete()
                    except Permission.DoesNotExist:
                        pass

        self.stdout.write('Field permissions update complete')
