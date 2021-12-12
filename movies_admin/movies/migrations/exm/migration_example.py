from django.db import models, migrations


def forwards_func(apps, schema_editor):
    # Этот код выполнится при применении миграции
    pass

def backwards_func(apps, schema_editor):
    # Этот код выполнится при отмене миграции
    pass


class Migration(migrations.Migration):
     dependencies = [
        ('app_name', '0001_initial'),
     ]
     operations = [
         migrations.RunPython(forwards_func, backwards_func),
     ]
