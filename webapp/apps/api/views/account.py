from rest_framework.response import Response
from rest_framework.views import APIView
from utils.constants import FriendStatus
from utils.constants import ResponseStatus as rs
from utils.helper import api_response
from utils.helper import get_account

#TODO: Possible race condition of sending requests at same time...

class SendFriendRequestView(APIView):
    """Sends friend request"""

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

class AcceptFriendRequestView(APIView):
    """Accepts friend request"""

    def post(self, request):
        other_account_id = request.POST['account_id']
        response_data = self.accept_request_helper(other_account_id)
        return Response(response_data)

    def accept_request_helper(self, other_account_id):
        current_account = self.request.user
        other_account = get_account(other_account_id)

        # Check if each other on friend's list
        if current_account.is_friends_with(other_account):
            return api_response(
                type='friend',
                view='accept_friend_request',
                status=rs.FAIL.value,
                message=f'Already have {other_account.username} as a friend',
            )

        # Check if friend requests are legitimate
        if current_account.can_add_friend(other_account):
            current_account.accept_friend_request(other_account)   # Current account accepts other account as friend
            return api_response(
                type='friend',
                view='accept_friend_request',
                status=rs.SUCCESS.value,
                message=f'Added {other_account.username} to friend list!',
            )
        return api_response(
            type='friend',
            view='accept_friend_request',
            status=rs.FAIL.value,
            message=f'Something went wrong trying to add {other_account.username}.',
        )

class RemoveFriendRequestView(APIView):
    """Unfriends a friend"""

    def post(self, request):
        other_account_id = request.POST['account_id']
        response_data = self.unfriend_request_helper(other_account_id)
        return Response(response_data)

    def unfriend_request_helper(self, other_account_id):
        current_user = self.request.user
        other_account = get_account(other_account_id)
        if current_user.is_friends_with(other_account):
            current_user.remove_friend(other_account)
            return api_response(
                type='friend',
                view='remove_friend_request',
                status=rs.SUCCESS.value,
                message=f'Removed {other_account.username} from friend list',
            )
        return api_response(
            type='friend',
            view='remove_friend_request',
            status=rs.FAIL.value,
            message=f'Unable to remove {other_account.username} from friend list',
        )

# TODO: Create block friend request... will be adding to a list, then for each view need to check if on block list...
