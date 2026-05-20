"""
Audit middleware.
Stores the current request user in thread-local storage
so models can access it for created_by / updated_by fields.
"""

import threading

_thread_locals = threading.local()


def get_current_user():
    """Return the user from the current request (used by signals or save overrides)."""
    return getattr(_thread_locals, 'user', None)


class AuditMiddleware:
    """Attach the authenticated user to the current thread for audit purposes."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            _thread_locals.user = request.user
        else:
            _thread_locals.user = None
        response = self.get_response(request)
        return response
