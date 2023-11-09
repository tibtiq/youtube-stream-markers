import os
from dataclasses import dataclass
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# todo rename broadcast to broadcast, thats the term youtube uses
@dataclass
class broadcastData:
    """Represents relevant data for a broadcast.

    Attributes:
        broadcast_id: ID of broadcast. Required for youtube live API calls.
        broadcast_description: Description of the broadcast
        scheduled_start_time: Scheduled start time of stream. Required for youtube live API calls.
    """
    broadcast_id: str
    broadcast_description: str
    scheduled_start_time: str


def get_broadcast_data(credentials: Credentials) -> broadcastData:
    """Gets relevant data from the latest broadcast.

    Args:
        credentials (Credentials): Credentials used for making youtube live API calls.

    Returns:
        broadcastData: Data containing relevant information to make API call.
    """
    with build('youtube', 'v3', credentials=credentials) as service:
        # pylint: disable=no-member
        response = service.liveBroadcasts().list(
            # filter for active ones, raise an error otherwise
            part='snippet',
            # required
            mine=True,
        ).execute()

    # get latest broadcast
    latest_broadcast = response['items'][0]

    return broadcastData(
        latest_broadcast['id'],
        latest_broadcast['snippet']['description'],
        latest_broadcast['snippet']['publishedAt'],
    )


def update_broadcast_description(credentials: Credentials, broadcast_data: broadcastData, new_description: str) -> None:
    """Updates broadcast description with new description.

    Args:
        credentials (Credentials): Credentials used for making youtube live API calls.
        broadcast_data (broadcastData): Data containing relevant information to make API call.
        new_description (str): Text to replace broadcast's current description.
    """
    with build('youtube', 'v3', credentials=credentials) as service:
        # pylint: disable=no-member
        response = service.liveBroadcasts().update(
            part='snippet',
            body={
                'id': broadcast_data.broadcast_id,
                'snippet': {
                    # required
                    'scheduledStartTime': broadcast_data.scheduled_start_time,
                    'description': new_description
                }
            }
        ).execute()


def main() -> None:
    SCOPES = [
        # get broadcast data
        'https://www.googleapis.com/auth/youtube.readonly',
        # modify broadcast description
        'https://www.googleapis.com/auth/youtube.force-ssl',
    ]
    # todo commandline argument
    if os.path.exists('token.json'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'token.json', scopes=SCOPES)
    else:
        exit(
            'Please obtain a OAuth client ID,'
            'rename it to token.json, and add it to same folder as script,'
            'https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth-installed.md#creating-application-credentials'
        )
    flow.run_local_server()
    credentials = flow.credentials

    broadcast_data = get_broadcast_data(credentials)
    print(broadcast_data)
    update_broadcast_description(
        credentials,
        broadcast_data,
        f'{broadcast_data.broadcast_description} IT WORKED AGAIN',
    )


if __name__ == "__main__":
    main()
