#!/usr/bin/env bash

set -eu

source $(dirname $0)/.env

# .env-local  is not under vc
if [ -f $(dirname $0)/.env-local ]; then
    source $(dirname $0)/.env-local
fi

# Note that the docker cache does not see updates on our env variables.
docker build --build-arg FEYNMAN_USER_ID=$FEYNMAN_USER_ID --rm -t rs/make .

docker_make () {
    targets="$@"

    docker run --rm \
       -v ${PWD}:/repo \
       --workdir=/repo \
       rs/make $targets
}
