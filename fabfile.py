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
        ../bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
    """.format(source_folder))
    # sudo('restart gunicorn-blog.sslinux.com')
    sudo('service nginx reload')
    print("--over--")

