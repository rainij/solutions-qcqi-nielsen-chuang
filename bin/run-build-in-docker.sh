#!/bin/bash

docker build --rm -t rs/make ./docker

docker run --rm \
       -v ${PWD}:/repo \
       --workdir=/repo \
       rs/make default
