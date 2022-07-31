# Microsoft Azure cloud resources:

Deploys via Docker container image:  
  - data lake blob storage   
  - mysql database   
  - databricks   
  - data factory   

## 1. Prerequisites

1.a) Docker
1.b) Azure Subscription

-----

## 2. Create Azure Data Lake Gen2, Azure MySQL, and Azure Data Factory base

The following steps setup an empty Data Lake, empty MySQL database server, and  
empty Data Factory instance.  

2.a) fill in secrets_template.ini based on your relevant Azure account configuration values, and save it as ".secrets".

2.b) to start azure cli container, run from local terminal:
`./start.sh`

2.c) now from inside azure cli container shell, run:   
`bash-5.1#./create_resources.sh`

2.d) login to az by entering given code at https://microsoft.com/devicelogin   

json metadata describing created resources will print to stdout.  Results should resemble that found in `execution_log_example.txt`.

----

## 3) Import Pipelines from ARM Template

To restore Data Factory to contain the three pipelines, we must import `arm_template.json`

3.a) Follow the directions in `Create_ADF_From_ARM_Template.pdf` ([original url](https://www.c-sharpcorner.com/article/create-a-copy-of-azure-data-factory-using-azure-arm-templates/))  

3.b) Import all of the python scripts from the `../scripts` directory to Databricks dbfs `Filestore` directory:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/databricks_import_scripts.png?raw=true)  


## 4) Initialize Database

To populate the Storm Events database with all of the available data, open the data factory pipeline "etl_all_files", and trigger it to run manually:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/trigger_now.png?raw=true)  

The monthly and yearly update pipelines are pre-configured to trigger on the necessary schedule, so no manually intervention is required.

## 5) Connect MySQL Workbench

To query the data, a dedicated query environment is desirable.  The most popular choice for MySQL was chosen in this case, MySQL Workbench.  

Install your operating system's version of MySQL workbench locally, and create a new connection to the Azure MySQL database:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/mysqlconfig.png?raw=true)  

###                   **Deployment Complete!**
