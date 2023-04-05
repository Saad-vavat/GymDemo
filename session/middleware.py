import json
from datetime import datetime

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the session has a last_activity key
        if 'last_activity' in request.session:
            # Get the last activity time from the session
            last_activity_time = request.session['last_activity']
            # Convert the time to a datetime object
            last_activity_time = datetime.fromisoformat(last_activity_time)

            # Check if the user has been inactive for longer than the timeout period
            timeout_seconds = 10
            if (datetime.now() - last_activity_time).total_seconds() > timeout_seconds:
                # If the user has timed out, delete the session and redirect to the login page
                del request.session['last_activity']
                del request.session['user_id']
                return redirect('/accounts/login/?next=' + request.path) 

        # Set the last activity time in the session
        request.session['last_activity'] = datetime.now().isoformat()

        response = self.get_response(request)
        return response

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError ("Type not serializable")
