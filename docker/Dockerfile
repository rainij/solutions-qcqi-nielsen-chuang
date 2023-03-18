FROM alpine:3.17

WORKDIR /workdir

RUN apk add git

RUN git clone --depth=1 git://git.sv.gnu.org/emacs.git --branch emacs-29 --single-branch emacs-29

ENTRYPOINT ["echo"]
