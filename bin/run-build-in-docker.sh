#!/bin/bash

docker build --rm -t rs/emacs ./docker

docker run --rm \
       -v ${PWD}:/repo \
       --workdir=/repo \
       rs/emacs default
