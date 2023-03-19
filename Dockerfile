FROM fedora:37

WORKDIR /workdir

RUN dnf -y install git

# #############################################################################
# Install a modern emacs
# #############################################################################

RUN git clone --depth=1 git://git.sv.gnu.org/emacs.git --branch emacs-29 --single-branch emacs-build

RUN dnf -y install 'dnf-command(builddep)' && \
    dnf -y builddep emacs
RUN cd emacs-build && \
    ./autogen.sh && \
    ./configure
RUN cd emacs-build && make -j3 && make install

# #############################################################################
# Setup python
# #############################################################################

# After this 'python' refers to the virtual env:
RUN python3 -m venv /opt/venv
ENV PATH /opt/venv/bin:$PATH

COPY src/requirements.txt src_requirements.txt
COPY test/requirements.txt test_requirements.txt
RUN python -m pip install -r src_requirements.txt -r test_requirements.txt

# #############################################################################
# End
# #############################################################################

# TODO:
# - remove repos
# - uninstall builddeps
#   - 'dnf-command(builddep)', make, git

# Cleanup
RUN rm -rf emacs-build
# TODO: can I remove some more of the build depenendencies of emacs?
RUN dnf -y remove 'dnf-command(builddep)'

# For local usage it makes sense to set this variable to your own UID (see the scripts in
# ./bin for more infos):
ARG FEYNMAN_USER_ID=1918
RUN useradd --uid $FEYNMAN_USER_ID feynman

ENTRYPOINT ["make"]
