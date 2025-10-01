from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_request import DeleteRequest
from ...models.delete_response import DeleteResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response
from ...http_utils import execute_request, execute_request_async


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: DeleteRequest,
) -> Dict[str, Any]:
    url = "{}/delete".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[DeleteResponse, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DeleteResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: DeleteRequest,
) -> Response[Union[DeleteResponse, HTTPValidationError]]:
    """delete remove erase

     Accepts ids  array each and optional filter to delete records.

    Args:
        json_body (DeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    return execute_request(
        client=client,
        kwargs=kwargs,
        parse_response_fn=_parse_response,
        build_response_fn=_build_response,
    )


def sync(
    *,
    client: AuthenticatedClient,
    json_body: DeleteRequest,
) -> Optional[Union[DeleteResponse, HTTPValidationError]]:
    """delete remove erase

     Accepts ids  array each and optional filter to delete records.

    Args:
        json_body (DeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: DeleteRequest,
) -> Response[Union[DeleteResponse, HTTPValidationError]]:
    """delete remove erase

     Accepts ids  array each and optional filter to delete records.

    Args:
        json_body (DeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    return await execute_request_async(
        client=client,
        kwargs=kwargs,
        parse_response_fn=_parse_response,
        build_response_fn=_build_response,
    )


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: DeleteRequest,
) -> Optional[Union[DeleteResponse, HTTPValidationError]]:
    """delete remove erase

     Accepts ids  array each and optional filter to delete records.

    Args:
        json_body (DeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
