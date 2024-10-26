""" A client library for accessing Long term memory """
import os

from .client import AuthenticatedClient, Client

def create_client(base_url, token):
    return AuthenticatedClient(
        base_url=base_url,
        token=token,
        verify_ssl=False,
        timeout=30.0
    )

__all__ = (
    "Client",
    "create_client",
)
