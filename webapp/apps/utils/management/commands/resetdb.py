import os
import glob
import sys
from os import listdir
from os.path import isfile, join
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

class Command(BaseCommand):
    '''
    Command that deletes all the migrations and the db file
    '''
    help = 'Resets the database'

    def handle(self, *args, **options):

        base = str(os.path.join(settings.BASE_DIR, 'apps'))
        migrations = glob.glob(os.path.join(base, "*", "migrations"))
        delete_migrations = input('Delete all migrations? y/N ')

        if delete_migrations == 'y' or delete_migrations == 'Y':
            for migration in migrations:
                for f in listdir(migration):
                    temp_file = join(migration, f)
                    if isfile(temp_file) and f != "__init__.py":
                        print(f"Successfully deleted: {str(temp_file)}")
                        os.remove(temp_file)
        '''
        delete_db = input('Delete database file? y/N ')
        if delete_db == 'y' or delete_db == 'Y':
            with connection.cursor() as cursor:
                cursor.execute("DROP SCHEMA public CASCADE;")
                cursor.execute("CREATE SCHEMA public;")
                os.system("python3 manage.py initdb")
        '''
        #os.system("python3 manage.py initdb")
        os.system("python3 manage.py makemigrations")
        os.system("python3 manage.py migrate")
        os.system("python3 manage.py createaccs")
