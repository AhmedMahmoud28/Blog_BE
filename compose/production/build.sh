#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

export GIT_HASH=$(git rev-parse --short HEAD);
docker-compose -f production.yml build
