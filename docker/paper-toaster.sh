#!/bin/bash
# Run paper-toaster and post-processing in a Docker container
#
# usage ./docker/paper-toaster.sh ARTWORK_ID [args]
REPO_ROOT=$(git rev-parse --show-toplevel)

mkdir -p $REPO_ROOT/workdir
BIND_WORKDIR="-v $REPO_ROOT/workdir:/workdir"

# If in "dev" environment, create bind mounts to hot-reload code without
# needing to rebuild the container
if [[ "$PAPER_TOASTER_ENV" = "dev" ]]
then
    BIND_SRC="-v $REPO_ROOT/src:/app"
    BIND_SCRIPTS="-v $REPO_ROOT/post-processing:/scripts"
fi

# Run the Python container to generate the Postscript file, then
# run the Ghostscript container to convert to PDF and PNG files.
ARTWORK_ID="$1"
docker container run $BIND_WORKDIR $BIND_SRC --rm -it ptrgags/paper-toaster $@ &&
docker container run $BIND_WORKDIR $BIND_SCRIPTS --rm -it ptrgags/post-toast-ghost $ARTWORK_ID.ps
