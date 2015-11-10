#!/bin/bash

set -e

## assume we have pip, virtualenv etc..


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "dir is ${DIR}"
TMP_DIR=${DIR}/../../.tmp
BUILD_BASE_DIR=${TMP_DIR}/build-wagon
ARTIFACTS_DIR=${TMP_DIR}/artifacts
PROJECT_BASE_DIR=${DIR}/../..

echo "cleaning build folder" && mkdir -p $BUILD_BASE_DIR && rm -rf $BUILD_BASE_DIR/*

pushd $BUILD_BASE_DIR

    echo "building virtualenv at `pwd`"
    VE_NAME=build-wagon-ve
    virtualenv $VE_NAME
    . $VE_NAME/bin/activate
popd

pip list

pushd $PROJECT_BASE_DIR
    echo "running pip install at `pwd`"

    pip install wagon



    mkdir -p ${ARTIFACTS_DIR}
    wagon create -s . -r dev-requirements.txt -o ${ARTIFACTS_DIR}

    # clean left overs from wagon
    rm -rf ${PROJECT_BASE_DIR}/wheelhouse

    ## todo: need to figure out how to construct the wheel

popd
