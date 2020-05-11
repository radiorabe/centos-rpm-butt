#!/bin/bash
#
# RPM build wrapper for audio, runs inside the build container on travis-ci

set -xe

OBS_OS=`source /etc/os-release; echo $ID`

case $OBS_OS in
"centos")
    OBS_DIST="CentOS_7"
    yum -y install \
        epel-release \
        http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
    ;;
"fedora")
    V=`source /etc/os-release; echo $VERSION_ID`
    OBS_DIST="Fedora_${V}"
    ;;
esac

curl -o /etc/yum.repos.d/apel.repo "https://download.opensuse.org/repositories/home:/radiorabe:/audio/${OBS_DIST}/home:radiorabe:audio.repo"

chown root:root butt.spec

rpmdev-setuptree

build-rpm-package.sh butt.spec
