""" Contains shared errors types that can be raised from API functions """


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(f"Unexpected status code: {status_code}")


class APIError(Exception):
    """Raised when an API request fails with a non-200 status code"""
    
    def __init__(self, status_code: int, content: bytes, message: str = None):
        self.status_code = status_code
        self.content = content
        self.message = message or f"API request failed with status code: {status_code}"
        super().__init__(self.message)


__all__ = ["UnexpectedStatus", "APIError"]
