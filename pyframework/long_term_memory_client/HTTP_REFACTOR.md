# HTTP Request Refactoring

## Overview

This refactoring eliminates code duplication across API endpoint files and improves error handling by introducing a centralized HTTP utilities module.

## Problems Solved

### 1. **Code Duplication**
Previously, every API endpoint file (`query_post.py`, `delete_delete.py`, `upsert_post.py`) contained identical code for making HTTP requests:

```python
response = httpx.request(
    verify=client.verify_ssl,
    **kwargs,
)
return _build_response(client=client, response=response)
```

### 2. **Poor Error Handling**
The old pattern silently returned `None` on failures, requiring manual checks:

```python
response = sync(client=client, json_body=query_request)
if response is None:
    return QueryResponse(results=[])  # Silent failure!
```

This approach:
- Hides errors from the caller
- Makes debugging difficult
- Requires boilerplate `if response is None` checks everywhere
- Doesn't distinguish between different failure types

## Solution

### New `http_utils.py` Module

Created a centralized module with:

1. **`execute_request()`** - Synchronous HTTP request execution
2. **`execute_request_async()`** - Asynchronous HTTP request execution
3. **`get_parsed_or_raise()`** - Safe response parsing with proper error handling
4. **`APIError`** - New exception class for API failures

### Key Benefits

#### ✅ **DRY Principle**
All HTTP request logic is now in one place, making maintenance easier.

#### ✅ **Explicit Error Handling**
Instead of returning `None`, the code now raises `APIError` with:
- Status code
- Response content
- Descriptive error message

#### ✅ **Better Developer Experience**
```python
# Old way - silent failure
response = sync(client=client, json_body=query_request)
if response is None:
    return QueryResponse(results=[])  # What went wrong? 🤷

# New way - explicit error
response = sync_detailed(client=client, json_body=query_request)
return get_parsed_or_raise(response)  # Raises APIError with details! 🎯
```

#### ✅ **Consistent Behavior**
All endpoints now handle errors the same way, making the API predictable.

## Changes Made

### 1. Created `http_utils.py`
New utility module with common HTTP request handling logic.

### 2. Updated `errors.py`
Added `APIError` exception class for non-200 status codes.

### 3. Refactored API Endpoints
Updated three files to use the new utilities:
- `api/default/query_post.py`
- `api/default/delete_delete.py`
- `api/default/upsert_post.py`

### 4. Fixed `query_long_term_memory()`
Changed from:
```python
response = sync(client=client, json_body=query_request)
if response is None:
    return QueryResponse(results=[])
return response
```

To:
```python
response = sync_detailed(client=client, json_body=query_request)
return get_parsed_or_raise(response)
```

Now properly raises `APIError` instead of silently returning empty results.

## Migration Guide

### For Callers of API Functions

**Before:**
```python
response = sync(client=client, json_body=request)
if response is None:
    # Handle error
    return default_value
# Use response
```

**After:**
```python
try:
    response = sync_detailed(client=client, json_body=request)
    result = get_parsed_or_raise(response)
    # Use result
except APIError as e:
    # Handle error with full context
    logger.error(f"API call failed: {e.status_code} - {e.message}")
    raise
```

### Error Handling Best Practices

1. **Catch `APIError` for expected failures** (e.g., validation errors)
2. **Let `UnexpectedStatus` propagate** for unexpected server errors
3. **Use `get_parsed_or_raise()`** to convert `Response` to parsed data safely

## Testing

Created `test_http_utils.py` with tests covering:
- ✅ Successful response parsing
- ✅ Error handling for failed requests
- ✅ Proper exception raising with status codes

## Future Improvements

1. Add retry logic to `execute_request()` for transient failures
2. Add request/response logging for debugging
3. Consider adding circuit breaker pattern for resilience
4. Add metrics collection for monitoring API health
