import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View

class GoogleCalendarInitView(View):
    def get(self, request):
        
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        scope = 'https://www.googleapis.com/auth/calendar'
        
        
        auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code'
        return redirect(auth_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        grant_type = 'authorization_code'
        token_url = 'https://accounts.google.com/o/oauth2/token'
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        }
        response = requests.post(token_url, data=data)
        access_token = response.json().get('access_token')
        
        calendar_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        events_response = requests.get(calendar_url, headers=headers)
        events = events_response.json().get('items', [])
        return JsonResponse(events, safe=False)        
