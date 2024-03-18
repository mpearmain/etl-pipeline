"""
Generic config module for the SDK based projects. The idea is all configuration is driven by environment variables
(possibly supplied via a .env file) with a fallback to AWS config manager.

The convention is to use env variables with all capitals and underscores as word delimiters.

Example:
     from etl-pipelines.src import config
     config.get('MY_FOO_SECRET')  # would return a value of environment variable MY_FOO_SECRET or AZURE secret of that
                                  # name or would raise an error if neither exists or is empty
    config.get('MY_FOO_SECRET', None)  # same as above but wont raise an error on missing value
"""
import datetime
import os
import pathlib
import typing

import dotenv

from {{ cookiecutter.repo_name }}.src.config import secrets_manager

dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True), verbose=True)

_KEYS: set[str] = set()
"""List of all keys ever requested through this config module (useful to create a template for an env file)."""

AZURE_ROOTCA: pathlib.Path = pathlib.Path(__file__).parent / "AzureRootCA1.pem"
"""Azure root certificate."""

AWS_ROOTCA: pathlib.Path = pathlib.Path(__file__).parent / "AwsRootCA1.pem"
"""AWS root certificate."""


def _get(factory: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[str], typing.Any]:
    """Getter builder with specific value type factory method.

    Args:
        factory: Type factory for casting value to the specific type.

    Returns: Value getter instance.
    """
    implicit = object()

    def getter(key: str, default: typing.Any = implicit) -> typing.Optional[str]:
        """Get the config option or return the explicit default value if not set. Note the implicit default value will
        raise an attribute error.

        Args:
            key: Option key to return.
            default: Value to be returned if option does not exist.

        Raises:
            ValueError if key not exists or has an empty value and no explicit default was provided.

        Returns:
            Option value or default.
        """
        _KEYS.add(key)
        value = os.getenv(key) or secrets_manager.get(key) or default
        if value is implicit:
            raise KeyError(f"Missing or empty value for option `{key}`. Please configure the environment.")
        if value is not None:
            value = factory(value)
        return value

    return getter


get = _get(str)
getint = _get(int)
getfloat = _get(float)
getseconds = _get(lambda v: datetime.timedelta(seconds=float(v)))
