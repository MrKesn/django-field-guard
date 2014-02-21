import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


__doc__="""
Django field guard
==============================

This app allows to add permissions for models' fields. The users who don't have permission to edit specified field will have this field read-only in django admin.

Installation
------------

Add ``fieldguard`` to ``INSTALLED_APPS``::

    # settings.py
    INSTALLED_APPS = (
        ...
        'django.contrib.admin',
        'fieldguard',
    )

Set ``@fieldguard.guard(field1, field2, ...)`` or ``@fieldguard.guard()`` decorator for desired model. Those fields ``field1``, ``field2`` etc. will be protected by the newly created rule::

    # shop/models.py
    ...
    import fieldguard
    
    ...
    @fieldguard.guard('name')
    class Product(models.Model):
        name = models.CharField(max_length=255)
        description = models.TextField(blank=True)
        quantity = models.PositiveIntegerField()
        price = models.PositiveIntegerField()

Set ``@fieldguard.enforce`` decorator for model's admin class. DO NOT FORGET TO ADD ``model`` which must specify the model class corresponding to current admin class. Set it even if the admin class is not InlineAdmin::
    
    # shop/admin.py
    ...
    import fieldguard
    from shop.models import Product
    
    ...
    @fieldguard.enforce()
    class ProductAdmin(admin.ModelAdmin)
        model = Product
        ...
    
    admin.site.register(Product, ProductAdmin)

Update django permissions db table::

    ./manage.py fgsync
    
Now go to the django admin page and edit any user's permissions. You will see there something like ``Can edit <model_name>[<field>]``.
From the example above, the rule will be ``Can edit Product[name]``.

Now any user who doesn't have the permission ``Can edit Product[name]`` sees field ``name`` as readonly.


"""

version = '0.1'

setup(
    name='django-field-guard',
    version=version,
    description='Add per field permissions',
    author='Alexandr Goncharov',
    author_email='kesn@yandex.ru',
    maintainer='Alexandr Goncharov',
    maintainer_email='kesn@yandex.ru',
    keywords='django model permission field',
    long_description=__doc__,
    url='https://github.com/MrKesn/django-field-guard',
    packages=['fieldguard'],
    include_package_data=True,
    platforms="any",
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
