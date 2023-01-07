import os

def save_superuser(username, email, password):
    os.system(f'python3 manage.py createadmin --username {username} --password {password} --noinput --email {email}')
    print(f"...added superadmin {username} to admin group")
    print(f"---------------------")
