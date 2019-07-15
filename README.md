[![Build Status](https://jenkins.liquiddemo.org/api/badges/CRJI/avere-europarl/status.svg)](https://jenkins.liquiddemo.org/CRJI/avere-europarl)

# avere-europarl

Scrape https://www.europarl.europa.eu/meps/

## Usage

### Install requirements

- Built on python-3.6.8

```shell
sudo apt update
sudo apt install python3 python3-pip
pip3 install Scrapy==1.6.0
```

### Run the program
```shell
cd scraper
./main.py
```
Creates a folder `./data/` where it will dump all the scraped data from every MEP

### Run with docker

```shell
./start.sh
```
It will create a folder `data`  with all the scraped information in it

### Arguments
```shell
./main.py --id 123456
```
This will create a folder called `TEST - 123456` in `./data/` where it will save the data scraped from the MEP with the `id` 123456

## How it works

### The scraper:

 1. gets names and IDs from https://www.europarl.europa.eu/meps/en/directory/xml

 2. for each page `https://www.europarl.europa.eu/meps/en/$ID`
   * gets all Declaration pdfs
     - e.g. 2 PDF files from https://www.europarl.europa.eu/meps/en/124831/ISABELLA_ADINOLFI/declarations#mep-card-content
   * for each section and subsection in the left pane, it saves a html file
     - e.g. curriculum-vitae.html for https://www.europarl.europa.eu/meps/en/124831/ISABELLA_ADINOLFI/cv#mep-card-content
     - the HTML content starts from the title, "Curriculum Vitae", until just above the next section, "Contact"

 3. saves data from each page in a folder which has the structure:

    - $root/scraper/data/
      - $MEP_FULL_NAME - $ID/
          * declaration1.pdf
          * declaration2.pdf
          * section1.html
          * section2.html
          * ...

 4. prints stats about what was done:
   - how many MEPs?
   - how many of them had pdfs looking like http://www.europarl.europa.eu/mepdif/124831_DFI_LEG9_rev0_IT.pdf under "Declarations"?

## Taking a look at the data

What is the total disk size of the output? - 1.7 GB

Do the results change when running on 3 days in a row?

Do we need to run OCR on any 2019 declarations?