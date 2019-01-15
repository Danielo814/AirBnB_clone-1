#!/usr/bin/python3
"""
creates and distributes an archive to web servers
"""
from fabric.operations import local, run, env
import os
from datetime import datetime

env.hosts = ['35.237.35.49', '34.73.18.193']


def do_pack():
    try:
        if os.path.exists("versions") is False:
            local("mkdir versions")
        created = datetime.now().strftime("%Y%m%d%H%M%S")
        tgzfile = "versions/web_static_{}.tgz".format(created)
        local("tar -cvzf {} web_static".format(tgzfile))
        return tgzfile
    except:
        return None


def do_deploy(archive_path):
    if os.path.exists(archive_path) is False:
        return False
    else:
        put(archive_path, "/tmp/")
        tgzfile = archive_path.split('/')[1]
        archivedir = tgzfile.split('.')[0]
        run("mkdir -p /data/web_static/releases/{}/"
            .format(archivedir))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgzfile, archivedir))
        run("rm /tmp/{}".format(tgzfile))
        run("mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/"
            .format(archivedir, archivedir))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archivedir))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archivedir))
        return True


def deploy():
    path = do_pack()
    if path is None:
        return False
    do_deploy(path)
