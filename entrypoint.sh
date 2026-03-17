#!/bin/bash

if ! getent group docker > /dev/null; then
    groupadd docker
fi

if [ -S /var/run/docker.sock ]; then
    chgrp docker /var/run/docker.sock
    chmod 660 /var/run/docker.sock
fi

exec su -c "/usr/local/bin/jenkins.sh" jenkins