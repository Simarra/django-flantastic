#-------------------------------------------------------------------------------------------------------------
# copyright (c) microsoft corporation. all rights reserved.
# licensed under the mit license. see https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------
from debian:10

# avoid warnings by switching to noninteractive
env debian_frontend=noninteractive

# or your actual uid, gid on linux if not the default 1000
arg username=vscode
arg user_uid=1000
arg user_gid=$user_uid

# configure apt and install packages
run apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # verify git, process tools, lsb-release (common in install instructions for clis) installed
    && apt-get -y install git procps lsb-release \
    #
    # create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
    && groupadd --gid $user_gid $username \
    && useradd -s /bin/bash --uid $user_uid --gid $user_gid -m $username \
    # [optional] uncomment the next three lines to add sudo support
    && apt-get install -y sudo \
    && echo $username all=\(root\) nopasswd:all > /etc/sudoers.d/$username \
    && chmod 0440 /etc/sudoers.d/$username

# geodjango packages
run apt-get -y install gdal-bin \
    python3 \
    python3-dev \
    libgdal-dev \
    binutils \
    wget \
    curl \
    libspatialite-dev \
    python3-venv \
    libsqlite3-mod-spatialite \
    # clean up
    && apt-get autoremove -y \
    && apt-get clean -y


# get pip and poetry
run wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py \
&& curl -ssl https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3



# make some useful symlinks that are expected to exist
run cd /usr/bin \
	&& { [ -e easy_install ] || ln -s easy_install-* easy_install; } \
	&& ln -s idle3 idle \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python3-config python-config


env path="${path}:/root/.poetry/bin"
# switch back to dialog for any ad-hoc use of apt-get

WORKDIR /usr/local/
ADD ./* /usr/local/

RUN source ${HOME}/.profile
run poetry install