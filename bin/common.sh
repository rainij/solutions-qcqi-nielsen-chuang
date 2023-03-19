#!/usr/bin/env bash

set -eu

# .env-local  is *not* under vc
if [ -f $(dirname $0)/.env-local ]; then
    source $(dirname $0)/.env-local
    ADDITIONAL_ARGS="--build-arg FEYNMAN_USER_ID=$FEYNMAN_USER_ID"
else
    ADDITIONAL_ARGS=""
fi

docker build $ADDITIONAL_ARGS --rm -t rs/make .

docker_make () {
    targets="$@"

    docker run --rm \
       -v ${PWD}:/repo \
       --workdir=/repo \
       rs/make $targets
}
