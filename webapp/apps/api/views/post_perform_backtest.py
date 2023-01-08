from rest_framework.response import Response
from rest_framework.views import APIView
from utils.helper import api_response

#TODO: Possible race condition of sending requests at same time...

class PostPerformBacktestView(APIView):
    """
    """

    def post(self, request):
        other_account_id = request.POST['account_id']
        response_data = self.send_request_helper(other_account_id)
        return Response(response_data)

    def send_request_helper(self, other_account_id):
        current_account = self.request.user
        other_account = get_account(other_account_id)

        # Check if friend requests have not been made yet
        if current_account.can_send_friend_request(other_account):
            current_account.send_friend_request(other_account)    # Sent request to other user...
            other_account.received_friend_request(current_account)  # Other account receives request.

            return api_response(
                type='friend',
                view='send_friend_request',
                status=rs.SUCCESS.value,
                message=f'Successfully sent friend request to {other_account.username}',
            )
        return api_response(
            type='friend',
            view='send_friend_request',
            status=rs.FAIL.value,
            message=f'Something went wrong sending friend request to {other_account.username}',
        )
