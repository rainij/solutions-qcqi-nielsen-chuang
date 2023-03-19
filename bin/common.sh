#!/usr/bin/env bash

set -eu

docker build --rm -t rs/make ./docker

docker_make () {
    targets="$@"

    docker run --rm \
       -v ${PWD}:/repo \
       --workdir=/repo \
       rs/make $targets
}
