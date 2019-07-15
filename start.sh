DIR="data"

if [ -d "$DIR" ]; then
    rm -rf $DIR
fi

mkdir $DIR

docker run --rm --name=scraper -v $PWD/data:/app/scraper/data liquidinvestigations/crji-avere-europarl python3 /app/scraper/main.py --id 124831