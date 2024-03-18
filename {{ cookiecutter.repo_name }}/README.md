{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        ├── config         <- All config parameters of the execution
             ├── AWSRootCA1.pem      <- AWS pem file
             ├── AzureRootCA1.pem    <- Azure pem file
             ├── logging.ini         <- logging config for new ETL pipeline
             ├── logging.py          <- logging setup
             ├── secrets_manager.py  <- retreive secrects from environment vars 
             ├── __init__.py         <- common isntantiation structure
        ├── client.py      <- Any external connection (via API for example) 
        ├── params.py      <- Any parameter settings required for the ETL process, (RAM for spark for example) 
        ├── pipeline.py    <- The ETL (extract-transform-load) pipeline itself containing the sequence of nodes
        │
        └── nodes          <- Scripts to containing each step of the ETL process.
             ├── data_gathering.py
             ├── data_preparation.py
             ├── data_storage.py
             ├── data_transform.py
             └── data_visualization.py
         
--------

