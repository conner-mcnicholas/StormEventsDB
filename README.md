# Storm Events Database
_____

## Background

  This cloud database of US storm events since 1950 is my official submission for the "Open Ended Capstone Project", part of the *Data Engineering* curriculum at __Springboard's School of Data__.

## Objective

  The objective of the Capstone is to identify a large raw dataset from which one could derive value, then develop and deploy a solution enabling the extraction, ingestion, and transformation of that data towards some practical application.

----

## Data Model  

There are three different schemas offering storm event data within csv.gz files:

#### Details
  - *columns:* 51
  - *rows:* ~1.8m (25k / year)
  - *description:* contains nearly all of the most essential data, including even location and fatality data, despite standalone files already being dedicated to those categories.

#### Locations  
  - *columns:* 11
  - *rows:* ~500k (7k / year)  
  - *description:* because the details file already includes all of the data that the location file contains, the locations file is descoped as it is not worth the storage and CPU cost.

#### Fatalities
  - *columns:* 11
  - *rows:* ~20 K (250 / year)  
  - *description:* although the details file even includes information about fatalities, the fatalities file provides further identifying information by documenting a single human fatality per row (identified by the compound primary key columns of EVENT_ID and FATALITY_ID) allowing indication of the deceased individual's age, sex, date of passing, etc.

### Entity Relationship Diagram:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/ERD.png?raw=true)  

-------

## Architecture

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/architecture_diagram.png?raw=true)  

---

## ELT Pipelines Overview:

To keep the database in sync with the latest data available, we must ingest new data as soon as it is available.  

There are three mechanisms by which new data is released and ingested through pipelines:  
> **Initial Load** (shorter: **initial** ; shortest: **init**)  
> **Monthly Update** (shorter: **update** ; shortest: **upd**)  
> **Yearly New** (shorter: **new** ; shortest: **new**)

1. **Initial Load**: is a simple ingestion of all available details and fatalities csv.gz files.  
    - "one and done", i.e. nothing to cleanup or monitor.
2. **Monthly Update**: On the 16th of each month, the current year's file is updated and renamed with mod date
    - upon confirmation of that filename change, trigger **upd** ELT pipeline  
3. **Yearly New**: On April 16th of each year, a fresh file for that year is dropped for the first time.  
    - Upon confirmation of that new file drop, trigger **new** ELT pipeline
    - Begin tracking this filename for monthly update, retiring last year's file  


The data extract logic required  for each exists in its respective python script  

(see:`scripts/*_files_to_blob*.py`)

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/pipeline_overview.png?raw=true)  

---

## Yearly New Pipeline Deep Dive:

  The **new** pipeline is the most involved, and taking a deep dive into that pipeline is instructive for all other cases:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/annotated_pull_new_w_id.png?raw=true)  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/yearly_deepdive.png?raw=true)  


**upd** and **new** pipelines conclude with Data Lake container maintenance  

(see: `scripts/datalake_housekeeping_*.py`):  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/clean_containers_output.png?raw=true)  

----

## Testing  

*General Tests* verify each year has a file in Data Lake for both tables  
*Pipeline Tests* verify each line from source files have rows in both tables

- **8** *Total Tests* = **2** *General Tests* + **6** *Pipeline Tests*
  - **2** *General Tests* = **1** *General Test* x **2** *Tables*
  - **6** *Pipeline Tests* = **3** *Pipeline Tests*  x **2** *Tables*

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/pipeline_test_success.png?raw=true)

----

## Deploying and Initializing Resources  

Instructions for initializing the database, ETL pipelines, and query environment are found in: `deploy_azure_resources/README.md`.

----

## Querying Data  

Available to explore -> 1.8M rows capturing 70 years of weather data across 62 *columns:*.  Perhaps creating a tighter view with limited columns is a good start...

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/create_view.png?raw=true)  

The analyst is now unencumbered in their exploration of this intriguing data set.  A warning, the data set *can* be slightly morbid:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/storm_deaths.png?raw=true)  

Results can be exported as csv and plotted using analyst's preferred tool.  For example, a simple time-series of deaths vs injuries by year using Google Sheets:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/graph.png?raw=true)  
