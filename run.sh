#!/usr/bin/bash

set -o errexit
set -o nounset

function usage() {
    cat <<EOF
Usage $0 OPTIONS DAY
Options:
    -a           run second part of the daily exercise
    --help, -h   this help
Day:
    day of the aoc exercise
EOF
}

if [[ $# != 1 && $# != 2 ]]; then
    usage
    exit 1
fi

ADVANCED=false
if [[ $# == 2 ]]; then
    case "$1" in
    -h | --help)
        usage
        exit 0
        ;;
    -a | --advanced)
        ADVANCED=true
        ;;
    *)
        echo "ERROR: Unknown option '$1'"
        usage
        exit 1
        ;;
    esac
    shift
fi

DAY=$1
if [[ ${ADVANCED} == false ]]; then
    ./curl-input.sh "${DAY}" | "./${DAY}/first.py"
else
    ./curl-input.sh "${DAY}" | "./${DAY}/second.py"
fi
