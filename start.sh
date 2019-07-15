#!/bin/bash -ex

cd "$( dirname "${BASH_SOURCE[0]}" )"

DIR="data"

if ! [ -d "$DIR" ]; then
    mkdir $DIR
fi

docker run --rm --user="$(id -u):$(id -g)" --name=scraper \
           -v "$PWD/data:/app/scraper/data" \
           liquidinvestigations/crji-avere-europarl \
           python3 /app/scraper/main.py
