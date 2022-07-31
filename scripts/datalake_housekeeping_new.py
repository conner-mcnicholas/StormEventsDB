from datetime import datetime,date,timedelta
import os
import sys
from pathlib import Path
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.storage.blob import ResourceTypes, AccountSasPermissions
from azure.storage.blob import generate_account_sas
import mysql.connector
from mysql.connector import errorcode

def cleanup_containers():
    CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]
    client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Create sas token for blob
    sas_token = generate_account_sas(
        account_name = client.account_name,
        account_key = ACCOUNT_KEY, # The account key for the source container
        resource_types = ResourceTypes(object=True, container=True),
        permission= AccountSasPermissions(read=True,list=True),
        start = datetime.now(),
        expiry = datetime.utcnow() + timedelta(hours=4) # Token valid for 4 hours
    )

    source_container_name = 'newfiles'
    source_container_client = client.get_container_client(source_container_name)

    destination_container_name = 'allfiles'
    destination_container_client = client.get_container_client(destination_container_name)

    for table in ['details','fatalities']:
        source_container_list = source_container_client.list_blobs()
        for s in source_container_list:
            #print('\n\nBEGIN SOURCE LOOP')
            #print(f'\ns: {s}')
            depth = len(Path(s.name).parts)
            #print(f'\ndepth check source: {depth}')
            if depth == 2:
                #print(f'SOURCE DEPTH PASSED')
                filetype = Path(s.name).parts[0]
                filename = Path(s.name).parts[-1]
                felements = filename.split("_")
                fyear = int(felements[3][1:5])
                #print(f'filename: {filename}')
                #print(f'fyear: {fyear}\n')
                if filetype == table:
                    newfile = filename
                    updateyear = fyear
                    new_blob_name = s.name
                    new_blob = client.get_blob_client(destination_container_name, new_blob_name)
                    # Create blob client for source blob
                    source_blob = BlobClient(
                        client.url,
                        container_name = source_container_name,
                        blob_name = new_blob_name,
                        credential = sas_token
                    )
                    print(f'{table} - COPYING updated file: {s.name} FROM source: {s.container} TO destination: {destination_container_name}')
                    new_blob.start_copy_from_url(source_blob.url)

                    print(f'{table} - DELETING updated file: {s.name} FROM source: {s.container}')
                    source_blob_dl = source_container_client.get_blob_client(s)
                    source_blob_dl.delete_blob()

def create_table_postcounts():
    config = {
      'host':f'{os.environ["AZ_MYSQL_SERVER_NAME"]}.mysql.database.azure.com',
      'user':f'{os.environ["AZ_MYSQL_ADMIN"]}@{os.environ["AZ_MYSQL_SERVER_NAME"]}',
      'password':os.environ["AZ_MYSQL_ADMIN_PASSWORD"],
      'database':'defaultdb',
      'client_flags': [mysql.connector.ClientFlag.SSL],
      'ssl_ca': f'{os.environ["HOME"]}/.ssh/DigiCertGlobalRootG2.crt.pem',
      'autocommit': True
    }

    query = (f"DROP TABLE IF EXISTS N_PostUpdate;"
        f"CREATE TABLE N_PostUpdate AS" # N for New File Pipeline
        "  SELECT * FROM"
        "	(SELECT COUNT(*) AS D_PostUpdate FROM details) AS d,"
        "	(SELECT COUNT(*) AS F_PostUpdate FROM fatalities) AS f;")

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.close()

cleanup_containers()

create_table_postcounts() #to compare to precounts in testing
