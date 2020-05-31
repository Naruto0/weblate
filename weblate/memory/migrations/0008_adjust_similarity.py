# Generated by Django 3.0.5 on 2020-05-12 11:44

from django.db import migrations


def update_index(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    # This ensures that extensions are loaded into the session. Without that
    # the next ALTER database fails unless we're running as superuser (which
    # is allowed to set non existing parameters, so missing extension doesn't
    # matter)
    # See https://www.postgresql.org/message-id/6376.1533675236%40sss.pgh.pa.us
    schema_editor.execute("SELECT show_limit()")

    schema_editor.execute(
        "ALTER DATABASE {} SET pg_trgm.similarity_threshold = 0.5".format(
            schema_editor.connection.settings_dict["NAME"]
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ("memory", "0007_use_trigram"),
    ]

    operations = [
        migrations.RunPython(
            update_index, migrations.RunPython.noop, elidable=False, atomic=False
        )
    ]
