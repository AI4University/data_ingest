# Tools for Ingestion of CORDIS data in AI4U Data Space

## **1. Download Cordis files**

The list of URLs to the Cordis files to download is provided in file `CORDISfiles.txt`. The download of the files can be carried out executing

```$ ./CORDISdownload.sh ./CORDISfiles.txt ./data/data_Pr_CORDIS/20220316```

The first parameter is the file containing the URLs of the files that will be downloaded, and the second parameter is the destination folder.

The script creates the destination folder, and under the given path it will also create subfolders `HORIZON`, `H2020`, `FP7`, and `cordis-ref`, where downloaded files will be organized.

## **2. Create CORDIS parquet files**

*2.1. Set up configuration file*

Copy config_default.cf as config.cf, and fill in the required information:

- `[cordis_data] -> dir_data` is the hdfs directory containing the files downloaded in step 1
- `[cordis_parquet] -> dir_parquet` is the hdfs directory where the parquet tables will be stored
- `[aux] -> dir_ss` is the hdfs directory where the semantic scholar `papers.parquet` table is stored
- `[aux] -> dir_patstat` is the hdfs directory where the PATSTAT `patstat_appln.parquet` table is stored

*2.2. Run the main script*

You are ready to go. How to lunch the script will depend on your Spark configuration. For us, this is:

    $ ./script-spark -C tokencluster.json -c 4 -N 10 -S CORDIS2parquet.py

