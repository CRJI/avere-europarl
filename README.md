[![Build Status](https://jenkins.liquiddemo.org/api/badges/CRJI/avere-europarl/status.svg)](https://jenkins.liquiddemo.org/CRJI/avere-europarl)

# avere-europarl

scrape https://www.europarl.europa.eu/meps/

## TODO - scraper

1. Add a .drone.yml file with flake8 check and click on the status icon above.

2. Use scrapy to set up a minimal crawler.

3. Implement the scraping:

 - get names and IDs from https://www.europarl.europa.eu/meps/en/directory/xml
 - for each page `https://www.europarl.europa.eu/meps/en/$ID`
   * get all Declaration pdfs
     - e.g. 2 PDF files from https://www.europarl.europa.eu/meps/en/124831/ISABELLA_ADINOLFI/declarations#mep-card-content
   * for each section and subsection in the left pane, save a html file
     - e.g. curriculum-vitae.html for https://www.europarl.europa.eu/meps/en/124831/ISABELLA_ADINOLFI/cv#mep-card-content
     - the HTML content should start from the title, "Curriculum Vitae", until just above the next section, "Contact"

   The scraper should download everything in a configurable folder which has the structure:

       - $root/
         - Isabella Adinofli - 124831/
           - 124831_DFI_LEG9_rev0_IT.pdf
           - 124831_ADINOLFI Isabella.pdf
           - curriculum-vitae.html
           - declarations.html
           - ...
           - 9th parlamentary term.html
           - 8th parlamentary term.html
         - ...      
 - print stats about what was done:
   - how many MEPs?
   - how many of them had pdfs looking like http://www.europarl.europa.eu/mepdif/124831_DFI_LEG9_rev0_IT.pdf under "Declarations"?  

4. After this is done, load the data into a new collection on https://hoover.liquiddemo.org.

## TODO - take a look at the data

What is the total disk size of the output?

Do the results change when running on 3 days in a row?

Do we need to run OCR on any 2019 declarations?
