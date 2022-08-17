# Benchmarking

I benchmarked elapsed times required for 9 different database technologies to ingest all 1.8 million rows across 51 columns of details data and execute 4 basic queries.

## Databases Included

 - Local MySQL: MySQL 8.0 running on my quad-core laptop  
 - Azure MySQL 8-core: MySQL 5.7 deployed on 8-core_Azure server  
 - Azure MySQL 1-core: MySQL 8.0 deployed on 1-core_Azure server  
 - PySpark Flat CSV Dataframe: Dataframe read from CSV on 8-node spark cluster  
 - PySpark Dataframe (8 partitions): Dataframe read from 8 explicit parquet partitions on 8-node spark cluster  
 - PySpark Dataframe (9 default partitions): Dataframe read from 9 parquet partitions chosen by default on 8-node spark cluster  
 - PySpark Dataframe (20 partitions): Dataframe read from 20 explicit parquet partitions on 8-node spark cluster  
 - Local q/KDB+: On-demand KDB+4.0 server running on my quad-core laptop  

The specifications for each is found below:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chart_db_specs.png?raw=true)  

#### Summary Groupings

The speeds were relatively consistent within the following 4 database categories, so results were averaged within these "groups" to summarize the general trend:

 - MySQL (includes Local, Azure 8-core, Azure 1-core)  
 - PySpark Flat CSV Dataframe (no grouping)  
 - PySpark Parquet Partitioned Dataframe (includes all dataframes created by reading from parquet files saved across any partition scheme)  
 - q/KDB+ (no grouping)  

## Results

The data ingestion, individual query, and grouped summary times are captured in the following table:

 ![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/charts_numbers.png?raw=true)

Chart of individual query times:  

 ![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chartquery.png?raw=true)

Grouped summary charts of query speed and ingestion speed, respectively (relative to slowest which is normalized at 1x):  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/groupedspeedcharts.png?raw=true)

If clarity is needed regarding the relationships between the raw numbers and the charts, reference diagram:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/charts_annotated.png?raw=true)


Given the use case of this project, wherein query speeds are of greater consequence than the infrequent data ingestion speeds, we find that the default
parquet partitioned pyspark dataframe and KDB+ offer the best performance profiles.  Kx Systems does not disclose any standard pricing for KDB+ deployments, but based on my experience it is unlikely to be a realistic contender.  Thus, using a PySpark dataframe built from partitioned parquet files is the most attractive technology for this stack.

#### TO-DO:

 - Orchestrate ETL with Airflow and
    - compare times to Azure Data Factory
