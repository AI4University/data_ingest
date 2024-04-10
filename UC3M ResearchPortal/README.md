# Working with the [UC3M Research Portal](https://researchportal.uc3m.es/)

> [!TIP]
> If you want to scrap any information from the site, create a local copy of the .html files (see how in the first section) in the  and execute your python pipeline from there, instead of making a request to the website every time.

> By scraping from the local files, you will avoid being kicked out of the site for requesting too many times.

## How to download the .html files locally
- First, install GNU wget in your terminal.
- Execute the following command to download all the resources from UC3M Research Portal:
```bash
$ wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --wait=1 --random-wait --domains researchportal.uc3m.es https://researchportal.uc3m.es/display/inv21546
```

## Contents
- `Research Portal Scraping.ipynb` contains the first draft of scraping for the Research Portal using Selenium.
- `ResearchPortal2parquet.ipynb` contains the final version of scraping for the Research Portal using BeautifulSoup.
> [!NOTE]  
> In the `Research Portal Scraping.ipynb` file, you can find (commented in the end) the procedure for matching the resulting data base after scraping with SCOPUS data base (to have as many 'abstracts' as possible after the crossing).

## Outputs
- `researchers.parquet`: Contains all the researchers from the Research Portal.
- `projects.parquet`: Contains all the projects from the Research Portal.
- `publications.parquet`: Contains all the publications from the Research Portal.
- `researchers_projects.parquet`: Crossing table (tabla de relación) between projects and researchers. It constains the researchers' IDs and projects' IDs (for each researcher and their corresponding projects).
- `researchers_publications.parquet`: Crossing table (tabla de relación) between publications and researchers. It constains the researchers' IDs and publications' IDs (for each researcher and their corresponding publications).

Last update (of tables): February, 2024.
