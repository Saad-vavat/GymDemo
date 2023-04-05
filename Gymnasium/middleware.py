from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        last_activity = request.session.get('last_activity')
        if last_activity:
            now = datetime.now()
            elapsed = (now - last_activity).seconds
            if elapsed > settings.SESSION_EXPIRE_SECONDS:
                messages.error(request, 'Your session has timed out. Please log in again.')
                del request.session['last_activity']
                return redirect(reverse('login'))

        request.session['last_activity'] = datetime.now()
        response = self.get_response(request)
        return response
