import os


class Config:
    """
    Config class.

    This class should be refactored out to be a general purpose config manager class available to all other projects.

    It should connect to the config manager and provide access to the configuration variables required.
    i.e the secrets manager or 

    """

    # pre-requeqs

    log_name = os.path.abspath('../log/{{ cookiecutter.logfile }}')

    # if this is set to True, then all the nodes will be automatically 
    # considered not up-to-date and will be rerun.
    force_execution = True 

    ## Database connection params
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = 'localhost'
    database = "{{ cookiecutter.database }}"

	
