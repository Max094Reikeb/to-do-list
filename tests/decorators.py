from functools import wraps


def tc(test_id: str):
    """Decorator to attach a test ID to a test method."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapper.test_case_id = test_id
        return wrapper

    return decorator
