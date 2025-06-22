"""
Default timezone configuration for the chat framework.
This can be overridden by importing and setting a custom get_timezone function.
"""

def get_timezone() -> str:
    """
    Default implementation that returns 'America/New_York'.
    Can be overridden by importing and setting a custom function.
    
    Returns:
        str: The default timezone string
    """
    return 'America/New_York'

# This can be imported and overridden by the agent project
_timezone_function = get_timezone

def set_timezone_function(func):
    """
    Set a custom timezone function.
    
    Args:
        func: A function that returns a timezone string
    """
    global _timezone_function
    _timezone_function = func

def get_current_timezone() -> str:
    """
    Get the current timezone using the configured timezone function.
    
    Returns:
        str: The current timezone string
    """
    return _timezone_function()
