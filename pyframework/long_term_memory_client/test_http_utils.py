"""Tests for the HTTP utilities module"""
import pytest
from http import HTTPStatus
from unittest.mock import Mock

import httpx

from .http_utils import get_parsed_or_raise, APIError
from .types import Response


def test_get_parsed_or_raise_with_valid_response():
    """Test that get_parsed_or_raise returns parsed data when available"""
    mock_parsed = {"result": "success"}
    response = Response(
        status_code=HTTPStatus.OK,
        content=b'{"result": "success"}',
        headers={},
        parsed=mock_parsed
    )
    
    result = get_parsed_or_raise(response)
    assert result == mock_parsed


def test_get_parsed_or_raise_with_none_parsed():
    """Test that get_parsed_or_raise raises APIError when parsed is None"""
    response = Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=b'{"error": "Bad request"}',
        headers={},
        parsed=None
    )
    
    with pytest.raises(APIError) as exc_info:
        get_parsed_or_raise(response)
    
    assert exc_info.value.status_code == 400
    assert "Bad request" in str(exc_info.value)


def test_get_parsed_or_raise_with_server_error():
    """Test that get_parsed_or_raise raises APIError with proper message for server errors"""
    response = Response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=b'Internal Server Error',
        headers={},
        parsed=None
    )
    
    with pytest.raises(APIError) as exc_info:
        get_parsed_or_raise(response)
    
    assert exc_info.value.status_code == 500
    assert "500" in str(exc_info.value)
