FROM fedora:37

WORKDIR /workdir

RUN dnf -y install git

RUN git clone --depth=1 git://git.sv.gnu.org/emacs.git --branch emacs-29 --single-branch emacs-29

ENTRYPOINT ["echo"]
