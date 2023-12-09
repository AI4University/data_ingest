# Tools for Ingestion of PATSTAT and CORDIS data in IntelComp Data Space

# **PATSTAT**

## **1. Download and prepare PATSTAT data**

PATSTAT files can be downloaded via web or, more conveniently, using the [getPATSTAT repository](https://github.com/IntelCompH2020/getPATSTAT). Follow instructions in the Readme file or such repository to dowload and uncompress PATSTAT Global into the local filesystem.

## **2. Ingest PATSTAT in a MYSQL database**

The ingestion of the PATSTAT dataset is based on the [load_patstat GitHub repository](https://github.com/simonemainardi/load_patstat) that has been modified to 1) Use InnoDB as default, and 2) Import only the most relevant tables files

Run `./load_patstat.sh` without parameters to display a brief help. Mandatory parameters are mysql_user and password, as well as MySQL database host and name. Optionally, a -v may be passed to obtain a verbose output. For testing purposes one may want to pass the modifier -t to only load small portions of zipped csv files. Output and error logs are written to output_log_YYYY-MM-DD and error_log_YYYY-MM-DD in the `./logs` directory. One may specify a different directory using the modifier -o.

    $ ./load_patstat.sh
    Usage: [-v] [-t] -u mysql_user -p mysql_pass -h mysql_host -d mysql_dbname -z patstat_zips_dir
        -v: be verbose
        -t: load small chunks of data for testing purposes
        -z: directory containing patstat files (defaults to ./data)
        -o: output and error logs directory (defaults to ./logs)
        -m: mysql data path (useful in combination with MyISAM engine)
        -e: mysql engine (defaults to InnoDB; changed from original project)

Therefore, standard use will be:

    $ ./load_patstat.sh -v -u <USER> -p <PASSWD> -h <HOST> -d db_Pa_PATSTAT <DBNAME> -z <PATH_TO_FILES> 
    
It is also important to note that the user must have permissions to create a new database in the MySQL server. Once the database has been created, it may be necessary to provide access to other users.

Troubleshooting: Using MyISAM engine, the utility must have write privileges into MySQL data folder. This is necessary to compress database tables and to work with table indices. Make sure the user that executes load_patstat.sh has such privileges.

## **3. Ingest PATSTAT as parquet files (independent of Step 2)**

*3.1. PATSTAT files conversion and upload to HDFS*

Zipped files provided by PATSTAT are not a good format to work with in Spark. For this reason, we should convert them to .gzip format. This can be done with the following commands that will place the gzipped files in directory `gz` under the current directory, and then upload everything to the Hadoop filesystem.

    $ for f in *.zip; do unzip -p "$f" | gzip -9 > "./gz/$(basename "$f" .zip).gz"; done
    $ hdfs -put ./gz/* /path/to/hdfs/dir

Note however that the conversion takes quite some time. This may not be the most efficient way to upload the tables in Spark. Alternatives to consider would be to:

- work directly with the uncompressed .csv files (roughly x6 space disk, around 400 GB in total) 

        $ unzip -d ./csv '*.zip'
        $ hdfs -put ./csv/* /path/to/hdfs/dir

- Uncompress the files to disk, convert in .gz files, and then delete the raw .csv files. This is a tradeoff between the two previous options.

*3.2. Set up configuration file*

Copy config_default.cf as config.cf, and fill in the required information in the `[spark]` section:

- `dir_data` is the hdfs directory containing the .gz of .csv files
- `dir_parquet` is the hdfs directory where the parquet tables will be stored

> [!IMPORTANT]
> From 2023 the pySpark script has been moved to the `legacy` folder and is no longer maintained. Only the `PATSTAT2parquet.ipynb` should be used.

*3.3. Run the main script* 

You are ready to go. How to lunch the script will depend on your Spark configuration. For us, this is:

    $ ./script-spark -C tokencluster.json -c 4 -N 10 -S PATSTAT2parquet.py

*3.4. Creating the parquet files with pySpark* 

All the code is available in notebook `PATSTAT2parquet.ipynb` that should be run in a pySpark cluster. The notebook is self-explanatory about some paths and options that need to be configured using some variables in that notebook.

The notebook currently creates the following parquet tables:

- `tls***.parquet`: All original tables available in the PATSTAT distribution
- `patstat_appln.parquet`: This is essentially a join of some of the previoous tables containing the most relevant information for topic modeling, and the most relevant metadata
- `npl_citations.parquet`: Table with links from patents to non-patent literature

Additionally, the notebook contains a specific section that can be used to filter patents according to keywords of CPC, which can be used to create specific target sets highly relevant for the living labs.

# **CORDIS**

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

