#!/usr/bin/bash

set -o errexit
set -o nounset

function usage() {
    cat <<EOF
Usage $0 OPTIONS DAY
Options:
    --help, -h   this help
Day:
    day of the aoc exercise
EOF
}

if [[ $# != 1 && $# != 2 ]]; then
    usage
    exit 1
fi

if [[ $# == 2 || $# == 1 ]]; then
    case "$1" in
    -h | --help)
        usage
        exit 0
        ;;
    *)
        if [[ $# == 2 ]]; then
            echo "ERROR: Unknown option '$1'"
            usage
            exit 1
        fi
        ;;
    esac
fi

DAY=$1

if [ -d "./${DAY}" ]; then
    echo "ERROR: Day ${DAY} already exists!"
    exit 1
fi

mkdir "${DAY}"
cp "template.py" "./${DAY}/first.py"
cp "template.py" "./${DAY}/second.py"
