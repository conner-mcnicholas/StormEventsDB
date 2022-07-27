# Storm Events Database

## Cloud database of storm events in the U.S. from 1950 - Present

_____

### Background

----

### Data Model

---

### Architecture

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/architecture_diagram.png?raw=true)  

---

### ELT Pipelines Overview:

To keep the database in sync with the latest data available, we must ingest new data as soon as it is available.  

There are three mechanisms by which new data is released and ingested through pipelines:  
> **Initial Load** (`......` or shortened as: **initial** `.....` or shortest as: **init**)  
> **Monthly Update** (`..` or shortened as: **update** `...` or shortest as: **upd**)  
> **Yearly New** (`......` or shortened as: **new** `......` or shortest as: **new**)

1. **Initial Load**: is a simple ingestion of all available details and fatalities csv.gz files.  
    - "one and done", i.e. nothing to cleanup or monitor.
2. **Monthly Update**: On the 16th of each month, the current year's file is updated and renamed with mod date
    - upon confirmation of that filename change, trigger **upd** ELT pipeline  
3. **Yearly New**: On April 16th of each year, a fresh file for that year is dropped for the first time.  
    - Upon confirmation of that new file drop, trigger **new** ELT pipeline_test_success
    - Begin tracking this file for monthly renaming, as it replaces last year's **upd** file

  The data extract logic required  for each exists in its respective python scripts  
  (see:`scripts/\*_files_to_blob\*.py`) and data factory tumbling window triggers

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/pipeline_overview.png?raw=true)  

---

### Yearly New Pipeline Deep Dive:

  The **new** pipeline is the most involved, and taking a deep dive into that pipeline is instructive for all other cases:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/annotated_pull_new_w_id.png?raw=true)  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/yearly_deepdive.png?raw=true)  

  **upd** and **new** pipelines conclude with Data Lake container maintenance as the final step  
  (see: `scripts/datalake_housekeeping_*.py`):

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/clean_containers_output.png?raw=true)  

----

### Testing  

  *General Tests* verify each year has a file in Data Lake for both table  
  *Pipeline Tests* verify each line from source files have rows in both MySQL tables

- **8** *Total Tests* = **2** *General Tests* + **6** *Pipeline Tests*
  - **2** *General Tests* = **1** *General Test* x **2** *Tables*
  - **6** *Pipeline Tests* = **3** *Pipeline Tests*  x **2** *Tables*

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/pipeline_test_success.png?raw=true)

----

### Query

- Available to explore -> 1.8M rows capturing 70 years of weather data across 62 columns:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/mysqlworkbench_detdate.png?raw=true)
