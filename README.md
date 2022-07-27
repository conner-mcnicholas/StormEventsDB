# Storm Events Database

## Cloud database of storm events in the U.S. from 1950 - Present

_____

### Background

### Data Model

### Architecture

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/Final/imgs/architecture_diagram.png?raw=true)  

### ELT Pipelines Overview:

To keep the database in sync with the latest data available, we must ingest new data as soon as it is make publicly available.  

There are three mechanisms under which data is released, referred to as **Initial Load*, **Monthly Update** and **Yearly New**,  
sometimes shortened as, respectively: **initial**,**update**, and **new**   
or even shorter as simply: **init**,**upd**, and **new**.

1. **Initial Load*: is a simple ingestion of all available details and fatalities csv.gz files.  
2. **Monthly Update*: On the 16th of each month, the current year's file is updated with the latest data
  - this is communicated by the source  filename changing to reflect the recently modified date.
    - upon confirmation of that filename change, trigger **upd** ELT pipeline  
3. **Yearly New*: On April 16th of each year, a fresh file for that year is dropped for the first time.  
  - This is communicated by generating a brand new file for the years
    - Upon confirmation of that new file drop, trigger **new** ELT pipeline_test_success
      - Begin tracking this file for monthly renaming, as it replaces last year's **upd** file

  A dedicated ELT pipeline has been tailored to each of these three distinct release cadences.  The data extract logic required
  for each exists in its respective python scripts (see:`scripts/\*_files_to_blob\*.py`), which are triggered by distinct
  tumbling window triggers in Azure Data Factory.  As the **upd** and **new** file pipelines are nearly identical, only differing with  
  respect to update frequency and repetition, taking a deep dive into the **new** pipeline will clarify the data flow for all cases.

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/annotated_pull_new_w_id.png?raw=true)  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/yearly_deepdive.png?raw=true)  

  **upd** and **new** pipelines conclude with Data Lake container maintenance as the final step (see: `scripts/datalake_housekeeping_*.py`):

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/clean_containers_output.png?raw=true)  

### Testing

- **8** *Total Tests* --> (**2 General Tests** + **6 Pipeline Tests**) ALL PASS SUCCESSFULLY (see: `testing/testing_plan_all_pipelines.txt`)
  - **2** *General Tests*  --> [**1** *General Test* x **2** *Tables*] verify that each year since 1950 is accounted for with a csvgz file in Data Lake  
  - **6** *Pipeline Tests* --> [**3** *Pipeline Tests*  x **2** *Tables*] verify that all rows in source csvgz file is accounted for with a row in MySQL table

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/pipeline_test_success.png?raw=true)

- Available to explore -> 1.8M rows capturing 70 years of weather data across 62 columns:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/mysqlworkbench_detdate.png?raw=true)
