"""Common HTTP utilities for making API requests with proper error handling"""
from http import HTTPStatus
from typing import Any, Callable, Dict, Optional, TypeVar

import httpx

from . import errors
from .client import Client
from .errors import APIError
from .types import Response

T = TypeVar("T")


def execute_request(
    *,
    client: Client,
    kwargs: Dict[str, Any],
    parse_response_fn: Callable[[Client, httpx.Response], Optional[T]],
    build_response_fn: Callable[[Client, httpx.Response], Response[T]],
) -> Response[T]:
    """
    Execute a synchronous HTTP request with proper error handling.
    
    Args:
        client: The API client
        kwargs: Request parameters (method, url, headers, etc.)
        parse_response_fn: Function to parse the response
        build_response_fn: Function to build the Response object
        
    Returns:
        Response object with parsed data
        
    Raises:
        errors.UnexpectedStatus: If the server returns an unexpected status code
        httpx.TimeoutException: If the request times out
        APIError: If the request fails with a non-200 status
    """
    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )
    
    return build_response_fn(client=client, response=response)


async def execute_request_async(
    *,
    client: Client,
    kwargs: Dict[str, Any],
    parse_response_fn: Callable[[Client, httpx.Response], Optional[T]],
    build_response_fn: Callable[[Client, httpx.Response], Response[T]],
) -> Response[T]:
    """
    Execute an asynchronous HTTP request with proper error handling.
    
    Args:
        client: The API client
        kwargs: Request parameters (method, url, headers, etc.)
        parse_response_fn: Function to parse the response
        build_response_fn: Function to build the Response object
        
    Returns:
        Response object with parsed data
        
    Raises:
        errors.UnexpectedStatus: If the server returns an unexpected status code
        httpx.TimeoutException: If the request times out
        APIError: If the request fails with a non-200 status
    """
    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)
    
    return build_response_fn(client=client, response=response)


def get_parsed_or_raise(response: Response[T]) -> T:
    """
    Extract parsed data from Response or raise an error if parsing failed.
    
    Args:
        response: The Response object
        
    Returns:
        The parsed data
        
    Raises:
        APIError: If the response could not be parsed (status code != 200)
    """
    if response.parsed is None:
        raise APIError(
            status_code=response.status_code.value,
            content=response.content,
            message=f"Request failed with status {response.status_code.value}: {response.content.decode('utf-8', errors='ignore')}"
        )
    return response.parsed
