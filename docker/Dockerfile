FROM fedora:37

WORKDIR /workdir

RUN dnf -y install git

RUN git clone --depth=1 git://git.sv.gnu.org/emacs.git --branch emacs-29 --single-branch emacs-build

RUN dnf -y install 'dnf-command(builddep)' && \
    dnf -y builddep emacs
RUN cd emacs-build && \
    ./autogen.sh && \
    ./configure
RUN cd emacs-build && make -j3 && make install

# TODO:
# - remove repos
# - uninstall builddeps
#   - 'dnf-command(builddep)', make, git

# Cleanup
RUN rm -rf emacs-build
# TODO: can I remove some more of the build depenendencies of emacs?
RUN dnf -y remove git 'dnf-command(builddep)'

ENTRYPOINT ["emacs"]
