#!/usr/bin/env bash

set -eu

# .env-local  is *not* under vc
if [ -f $(dirname $0)/.env-local ]; then
    source $(dirname $0)/.env-local
    ADDITIONAL_BUILD_ARGS="--build-arg FEYNMAN_USER_ID=$FEYNMAN_USER_ID"
    ADDITIONAL_RUN_ARGS="--user feynman"
else
    ADDITIONAL_BUILD_ARGS=""
    ADDITIONAL_RUN_ARGS=""
fi

docker build $ADDITIONAL_BUILD_ARGS --rm -t rs/make .

docker_make () {
    targets="$@"

    docker run --rm $ADDITIONAL_RUN_ARGS \
       -v ${PWD}:/repo \
       --workdir=/repo \
       rs/make $targets
}
