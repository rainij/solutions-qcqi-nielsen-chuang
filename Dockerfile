# #############################################################################
# This stage just builds an emacs which is newer than fedoras
# #############################################################################
FROM fedora:37 as build-emacs

WORKDIR /workdir

RUN dnf -y install git

RUN git clone --depth=1 git://git.sv.gnu.org/emacs.git --branch emacs-29 --single-branch emacs-build

RUN dnf -y install 'dnf-command(builddep)' && \
    dnf -y builddep emacs
RUN cd emacs-build && \
    ./autogen.sh && \
    ./configure --prefix /opt/emacs --without-all && \
    make -j3 && make install

# #############################################################################
# The actual image
# #############################################################################
FROM fedora:37

COPY --from=build-emacs /opt/emacs /opt/emacs
ENV PATH /opt/emacs/bin:$PATH
# Dirty hack: we just install fedoras emacs for the dependencies:
RUN dnf -y install --setopt=install_weak_deps=False git make emacs && dnf clean all && \
  rpm -e --nodeps emacs

# After this 'python' refers to the virtual env:
RUN python3 -m venv /opt/venv
ENV PATH /opt/venv/bin:$PATH

COPY src/requirements.txt src_requirements.txt
COPY test/requirements.txt test_requirements.txt
RUN python -m pip install --no-cache-dir -r src_requirements.txt -r test_requirements.txt

# For local usage it makes sense to set this variable to your own UID (see the scripts in
# ./bin for more infos):
ARG FEYNMAN_USER_ID=1918
RUN useradd --uid $FEYNMAN_USER_ID feynman

ENTRYPOINT ["make"]
