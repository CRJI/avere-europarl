#!/bin/bash -ex

cd "$( dirname "${BASH_SOURCE[0]}" )"
set +e
DIR="data"

if ! [ -d "$DIR" ]; then
    mkdir $DIR
fi

test_arg=""
if [ $# -eq 1 ]; then
    test_arg="--id $1"
fi

docker run --rm --user="$(id -u):$(id -g)" --name=scraper \
           -v "$PWD/data:/app/scraper/data" \
           liquidinvestigations/crji-avere-europarl \
           python3 /app/scraper/main.py $test_arg
