# centos-rpm-butt
CentOS 7 RPM Specfile for [butt](http://danielnoethen.de/) (broadcast using this tool) which is part of [Radio Bern RaBe's Audio Packages for Enterprise Linux (RaBe APEL)](https://build.opensuse.org/project/show/home:radiorabe:audio).

## Usage
There are pre-built binary packages for CentOS 7 available on [RaBe APEL package repository](https://build.opensuse.org/project/show/home:radiorabe:audio), which can be installed as follows:

```bash
# Add EPEL repository
yum install epel-release

# Add Nux Dextop repository
yum install http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm

# Add RaBe APEL repository
curl -o /etc/yum.repos.d/home:radiorabe:audio.repo \
     http://download.opensuse.org/repositories/home:/radiorabe:/audio/CentOS_7/home:radiorabe:audio.repo
 
 # Add Radio RaBe Streambox repository if you want a modern Opus codec version
 curl -o /etc/yum.repos.d/home:radiorabe:streambox.repo \
     http://download.opensuse.org/repositories/home:/radiorabe:/streambox/CentOS_7/home:radiorabe:streambox.repo

# Install butt
yum install butt
```
