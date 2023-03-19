#!/usr/bin/env bash

set -eu

# .use_feynman is *not* under vc. Create this file with a single line
# "FEYNMAN_USER_ID=<your UID>" to use the scripts run-*-in-docker.sh locally without
# permission conflicts (so that generated files/folders like ./public/ have the correct
# owner). This may be convenient for example if you do not have emacs installed but still
# want to tangle all files or build the site locally.
if [ -f $(dirname $0)/.use_feynman ]; then
    source $(dirname $0)/.use_feynman
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
