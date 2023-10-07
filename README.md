# data_ingest
Jupyter notebooks with the automatized process to obtain the necessary databases.

## Research Portal: downloading the resources
- First, install GNU wget in your terminal.
- Execute the following command to download all the resources from UC3M Research Portal:
```bash
$ wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --wait=1 --random-wait --domains researchportal.uc3m.es https://researchportal.uc3m.es/display/inv21546
```
  
