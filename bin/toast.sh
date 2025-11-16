#!/bin/bash
set -e

pushd src
python -m papertoaster $@
popd
