[![Build Status](https://jenkins.liquiddemo.org/api/badges/CRJI/avere-europarl/status.svg)](https://jenkins.liquiddemo.org/CRJI/avere-europarl)

# avere-europarl

scrape https://www.europarl.europa.eu/meps/

### TODO

Add a .drone.yml file with flake8 check and click on the status icon above.

Use scrapy to set up a minimal crawler.

Implement the scraping:

- get names and IDs from https://www.europarl.europa.eu/meps/en/directory/xml
- for each page https://www.europarl.europa.eu/meps/en/$ID
  * get all Declaration pdfs (https://www.europarl.europa.eu/meps/en/124831/ISABELLA_ADINOLFI/declarations#mep-card-content)
  * for each section and subsection in the left pane, save a html file (curriculum-vitae.html for https://www.europarl.europa.eu/meps/en/124831/ISABELLA_ADINOLFI/cv#mep-card-content) with the HTML content (starting from the title, "Curriculum Vitae", until just above the next section "Contact", so we don't get content duplication with the header/footer)
  
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
