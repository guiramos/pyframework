from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models import QueryRequest, HTTPValidationError, QueryResponse
from ...models.query_response import get_top_results_above_threshold
from ...types import Response, UNSET


def _get_kwargs(
        *,
        client: AuthenticatedClient,
        json_body: QueryRequest,
) -> Dict[str, Any]:
    url = "{}/query".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, QueryResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, QueryResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
        *,
        client: AuthenticatedClient,
        json_body: QueryRequest,
) -> Response[Union[HTTPValidationError, QueryResponse]]:
    """query search lookup

     Accepts search query objects array each with query and optional filter. Break down complex questions
    into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split
    queries if ResponseTooLargeError occurs.

    Args:
        json_body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, QueryResponse]]
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
        json_body: QueryRequest,
) -> Optional[Union[HTTPValidationError, QueryResponse]]:
    """query search lookup

     Accepts search query objects array each with query and optional filter. Break down complex questions
    into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split
    queries if ResponseTooLargeError occurs.

    Args:
        json_body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, QueryResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
        *,
        client: AuthenticatedClient,
        json_body: QueryRequest,
) -> Response[Union[HTTPValidationError, QueryResponse]]:
    """query search lookup

     Accepts search query objects array each with query and optional filter. Break down complex questions
    into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split
    queries if ResponseTooLargeError occurs.

    Args:
        json_body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, QueryResponse]]
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
        json_body: QueryRequest,
) -> Optional[Union[HTTPValidationError, QueryResponse]]:
    """query search lookup

     Accepts search query objects array each with query and optional filter. Break down complex questions
    into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split
    queries if ResponseTooLargeError occurs.

    Args:
        json_body (QueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, QueryResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed


def query_long_term_memory(client, query, user_id=None, document_id=None, source_id=None, source=None,
                           reference=None, doc_type=None,
                           k=1) -> QueryResponse:
    criteria = f"{query}".replace("_", " ")

    filter_dict = {}
    if user_id is not None:
        filter_dict["user_id"] = f"{user_id}"
    if document_id is not None:
        filter_dict["document_id"] = f"{document_id}"
    if source is not None:
        filter_dict["source"] = f"{source}"
    if source_id is not None:
        filter_dict["source_id"] = f"{source_id}"
    if reference is not None:
        filter_dict["reference"] = f"{reference}"
    if doc_type is not None:
        filter_dict["doc_type"] = f"{doc_type}"

    query_payload = {
        "queries": [
            {
                "query": f"{criteria}",
                "filter": filter_dict if filter_dict else UNSET,
                "top_k": k
            }
        ]
    }

    query_request = QueryRequest.from_dict(query_payload)
    response = sync(client=client, json_body=query_request)
    if response is None:
        return QueryResponse(results=[])
    return response


def query_long_term_top_results(client, query, user_id=None, document_id=None, source_id=None, source=None, reference=None,
                                doc_type=None,threshold=0.3, k=3):
    long_term_response = query_long_term_memory(client, query, user_id, document_id, source_id, source, reference, doc_type, k)
    return get_top_results_above_threshold(long_term_response, threshold, k)
