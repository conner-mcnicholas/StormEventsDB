# DEPLOYING AND INITIALIZING AZURE RESOURCES


## 1. Prerequisites

1.a) Docker  

1.b) Azure Subscription

-----

## 2. Create Azure Data Lake Gen2, Azure MySQL, and Azure Data Factory base

Deploys via Docker container image:  
  - data lake blob storage   
  - mysql database   
  - databricks   
  - data factory   

2.a) fill in secrets_template.ini based on your relevant Azure account configuration values, and save it as ".secrets".

2.b) to start azure cli container, run from local terminal:
`./start.sh`

2.c) now from inside azure cli container shell, run:   
`bash-5.1#./create_resources.sh`

2.d) login to az by entering given code at https://microsoft.com/devicelogin   

json metadata describing created resources will print to stdout.  Results should resemble that found in `execution_log_example.txt`.

----

## 3) Configure Databricks

Before restoring Data Factory to contain the three pipelines, we must first configure Databricks  

3.a) Create cluster in Databricks, with environment variables added referencing: `cluster_config.ini`  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/databricks_cluster_setup.png?raw=true)  

3.b) Take note of your cluster id from its config json:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/databricks_find_cluster_id.png?raw=true)  

3.c) Import all of the python scripts from the `../scripts` directory to Databricks dbfs `FileStore` directory:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/databricks_import_scripts.png?raw=true)  

---

## 4) Import Pipelines from ARM Template

Now we can populate ADF with our three pipelines using the ARM template.  

4.a) At the beginning of arm_template.json, replace the 3 placeholders for with your own config values from .secrets + cluster-id from step 3b.  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/datafactory_replace_template.png?raw=true)  

4.b) To import the ARM template into ADF, follow instructions in `Create_ADF_From_ARM_Template.pdf` ([original url](https://www.c-sharpcorner.com/article/create-a-copy-of-azure-data-factory-using-azure-arm-templates/))  

---

## 5) Initialize Database

To populate the Storm Events database with all of the available data, open the data factory pipeline "etl_all_files", and trigger it to run manually:

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/trigger_now.png?raw=true)  

The monthly and yearly update pipelines are pre-configured to trigger on the necessary schedule, so no manually intervention is required.  

---

## 6) Connect MySQL Workbench

To query the data, a dedicated query environment is desirable.  The most popular choice for MySQL was chosen in this case, MySQL Workbench.  

Install your operating system's version of MySQL workbench locally, and create a new connection to the Azure MySQL database:  

![alt text](https://github.com/conner-mcnicholas/StormEventsDB/blob/main/imgs/mysqlconfig.png?raw=true)  

#----------------------**Deployment Complete!**----------------------------
