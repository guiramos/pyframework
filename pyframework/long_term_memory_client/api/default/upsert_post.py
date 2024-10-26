from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.upsert_request import UpsertRequest
from ...models.upsert_response import UpsertResponse
from ...types import Response


def _get_kwargs(
        *,
        client: AuthenticatedClient,
        json_body: UpsertRequest,
) -> Dict[str, Any]:
    url = "{}/upsert".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
        *, client: Client, response: httpx.Response
) -> Optional[Union[HTTPValidationError, UpsertResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpsertResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UpsertResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
        *,
        client: AuthenticatedClient,
        json_body: UpsertRequest,
) -> Response[Union[HTTPValidationError, UpsertResponse]]:
    """upsert insert update remember

     Save and remember information for late use. Accepts an array of documents with text (potential
    questions + conversation text), metadata (source 'chat' and timestamp, no ID as this will be
    generated). Confirm with the user before saving, ask for more details/context.

    Args:
        json_body (UpsertRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UpsertResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
        *,
        client: AuthenticatedClient,
        json_body: UpsertRequest,
) -> Optional[Union[HTTPValidationError, UpsertResponse]]:
    """upsert insert update remember

     Save and remember information for late use. Accepts an array of documents with text (potential
    questions + conversation text), metadata (source 'chat' and timestamp, no ID as this will be
    generated). Confirm with the user before saving, ask for more details/context.

    Args:
        json_body (UpsertRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UpsertResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
        *,
        client: AuthenticatedClient,
        json_body: UpsertRequest,
) -> Response[Union[HTTPValidationError, UpsertResponse]]:
    """upsert insert update remember

     Save and remember information for late use. Accepts an array of documents with text (potential
    questions + conversation text), metadata (source 'chat' and timestamp, no ID as this will be
    generated). Confirm with the user before saving, ask for more details/context.

    Args:
        json_body (UpsertRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UpsertResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
        *,
        client: AuthenticatedClient,
        json_body: UpsertRequest,
) -> Optional[Union[HTTPValidationError, UpsertResponse]]:
    """upsert insert update remember

     Save and remember information for late use. Accepts an array of documents with text (potential
    questions + conversation text), metadata (source 'chat' and timestamp, no ID as this will be
    generated). Confirm with the user before saving, ask for more details/context.

    Args:
        json_body (UpsertRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UpsertResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed


def upsert_information(client, document_id, text, source_id, created_at, author, source="chat"):
    upsert_payload = {
        "documents": [
            {
                "text": text,
                "metadata": {
                    "source": source,
                    "source_id": source_id,
                    "created_at": created_at,
                    "author": author,
                }
            }
        ]
    }

    if document_id is not None and document_id != "":
        upsert_payload["documents"][0]["id"] = document_id
        upsert_payload["documents"][0]["metadata"]["document_id"] = document_id

    upsert_request = UpsertRequest.from_dict(upsert_payload)
    return sync(client=client, json_body=upsert_request)
