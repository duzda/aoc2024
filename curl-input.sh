#!/usr/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Please supply day" 1>&2
    exit 1
fi

DAY=$1

COOKIE=$(<.cookie)
# Strip newline
COOKIE=$(echo "${COOKIE}" | tr --delete '\n')
if [[ -z "$COOKIE" ]]; then
    echo "Please create .cookie file and supply your cookie" 1>&2
    exit 1
fi

curl --show-error --silent "https://adventofcode.com/2024/day/${DAY}/input" --header "Cookie: session=${COOKIE}"
