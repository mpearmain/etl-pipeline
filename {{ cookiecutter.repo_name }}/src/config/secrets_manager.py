"""
Secret manager implementation.
"""
import logging
import os
import typing

import boto3
from botocore.exceptions import ClientError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

LOGGER = logging.getLogger(__name__)

PREFIX = "{{ cookiecutter.repo_name}}_"
SECRET_SOURCE = os.getenv("SECRET_SOURCE", "AWS")  # Can be "AWS" or "AZURE"


def get(key: str) -> typing.Optional[str]:
    """Get the given secret from the manager.

    Args:
        key: {{cookiecutter.repo_name}} config key.

    Return:
        Actual secret value if it exists.
    """
    secret_id = key2id(key)
    secret_value = fetch_secret(secret_id)
    if secret_value is None:
        LOGGER.debug("Secret with id: %s not found", secret_id)
    return secret_value


def fetch_secret(secret_id: str) -> typing.Optional[str]:
    """Fetch secret value using the appropriate cloud provider."""
    if SECRET_SOURCE == "AWS":
        return _aws_call(secret_id)
    elif SECRET_SOURCE == "AZURE":
        secret = _azure_call(secret_id)
        return secret.get("value") if secret else None
    else:
        LOGGER.error("Unsupported secret source: %s", SECRET_SOURCE)
        return None


def _aws_call(secret_id: str) -> typing.Optional[dict[str, typing.Any]]:
    """Get secret value from AWS."""
    client = boto3.client("secretsmanager", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
    try:
        response = client.get_secret_value(SecretId=secret_id)
        return {"value": response.get("SecretString")}
    except ClientError as err:
        if err.response["Error"]["Code"] in {"ResourceNotFoundException", "InvalidRequestException"}:
            return None
        raise


def _azure_call(secret_name: str) -> dict:
    """Get secret value from Azure Key Vault."""
    key_vault_url = os.getenv("AZURE_KEYVAULT_URL")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    try:
        secret = client.get_secret(secret_name)
        return {"value": secret.value}
    except (ResourceNotFoundError, HttpResponseError) as err:
        LOGGER.debug("Azure error fetching secret %s: %s", secret_name, str(err))
        return None


def key2id(key: str) -> str:
    """Create a secret ID for the given key."""
    return f"{PREFIX}{key}" if not key.startswith(PREFIX) else key
