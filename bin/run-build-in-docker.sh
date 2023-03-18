#!/bin/bash

docker build --rm -t rs/emacs ./docker

docker run --rm rs/emacs --version
