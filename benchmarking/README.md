# Benchmarking

I benchmarked elapsed times required for 9 different database technologies to ingest all 1.8 million rows across 51 columns of details data and execute 4 basic queries.

## Databases Included

 - Local MySQL: MySQL 8.0 running on my quad-core laptop  
 - Azure MySQL 8-core: MySQL 5.7 deployed on 8-core_Azure server  
 - Azure MySQL 1-core: MySQL 8.0 deployed on 1-core_Azure server  
 - Databricks Flat CSV Dataframe: Dataframe read from CSV on 8-node spark cluster  
 - Databricks Dataframe (8 partitions): Dataframe read from 8 explicit parquet partitions on 8-node spark cluster  
 - Databricks Dataframe (9 default partitions): Dataframe read from 9 parquet partitions chosen by default on 8-node spark cluster  
 - Databricks Dataframe (20 partitions): Dataframe read from 20 explicit parquet partitions on 8-node spark cluster  
 - Local q/KDB+: On-demand KDB+4.0 server running on my quad-core laptop  

The specifications for each is found below:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chart_db_specs.png?raw=true)  

#### Summary Groupings

The speeds were relatively consistent within the following 4 database categories, so results were averaged within these "groups" to summarize the general trend:

 - MySQL (includes Local, Azure 8-core, Azure 1-core)  
 - Databricks Flat CSV Dataframe (no grouping)  
 - Databricks Parquet Partitioned Dataframe (includes all dataframes created by reading from parquet files saved across any partition scheme)  
 - q/KDB+ (no grouping)  

## Results

The data ingestion, individual query, and grouped summary times are captured in the following table:

 ![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chart_numbers.png?raw=true)

Chart of individual query times:  

 ![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chartquery.png?raw=true)

Chart of query time grouped summary:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chartqueryspeed.png?raw=true)

Chart of ingestion time grouped summary:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/chartingestspeed.png?raw=true)

If clarity is needed regarding the relationships between the raw numbers and the charts, reference diagram:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/benchmarking/imgs/charts_annotated.png?raw=true)