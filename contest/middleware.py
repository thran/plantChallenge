from django.http import JsonResponse

from contest.views import allow_user_to_contest


class UserMiddleware:
    def process_response(self, request, response):
        if request.path == "/user/profile/":
            response.content = response.content.replace('"staff":', '"contest_open": {}, "staff":'.format(
                "true" if allow_user_to_contest(request.user) else "false"
            ))

            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)

        return response
