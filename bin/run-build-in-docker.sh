#!/bin/bash

docker build --rm -f docker/Dockerfile -t rs/emacs .

docker run --rm rs/emacs
