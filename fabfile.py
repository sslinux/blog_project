from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "https://github.com/sslinux/blog_project.git"

env.user = "xgy"
env.password = "6525876As>?"

env.hosts = ['192.168.1.15']
env.port = '22'

def deploy():
    source_folder = '/home/xgy/sites/blog.sslinux.com/blog_project'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirement.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py makemigrations &&
        ../env/bin/python3 manage.py migrate &&
        ../env/bin/gunicorn --bind 127.0.0.1:8000 blog_project.wsgi:application
    """.format(source_folder))
    sudo('service nginx reload')
    print("--over--")
