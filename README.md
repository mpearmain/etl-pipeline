# ETL CookieCutter
A repo designed to give structure to each new ETL job that runs, in a consistent way for the user

## USAGE:

### Install cookiecutter if you don't have it.

> `pip install cookiecutter` or
> `poetry add cookiecutter`

### To start a new project run:

> `cookiecutter https://github.com/mpearmain/etl-pipeline`

for unix users or 

> `cookiecutter.exe https://github.com/mpearmain/etl-pipelines`

for windows users.

This will create a file organization in the following structure:
Please note, there is no `DATA` structure to this project, we have purposefully excluded folders to store data in as 
this should be configuration.  this means that both the ingress and egress physical location can change based on the 
external factors. 

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

## General Structure

The general idea is to centralise all steps of the pipeline in the nodes directory (submodule), the configuration in the `config.py` and `params.py` files, the connection in the `client.py` file and the pipeline itself on the `pipeline.py` file. 
- Always specify in `config.py`  how we connect, read, write to data sources, this should include data contracts
- Always specify in `params.py` the specific pipeline settings

## Documentation

The initial documentation is also already updated. One can create the documentation by entering docs and typing: 
> `./make.bat`
for windows users and 
> `./make` 
for unix users. 

Also, to run the documentation as is, you'll have to install a requirement. To do that, just type 

> `pip install -r requirements.txt`
