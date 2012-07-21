import os
import sys
import fileinput

try:
    url = os.environ['DATABASE_URL']

    for line in fileinput.input('alembic.ini', inplace=1):
        sys.stdout.write(line.replace('postgresql://raid:cloud@localhost/raidcloud', url))

except KeyError:
    pass

os.system('alembic upgrade head')
