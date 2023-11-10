# todo turn this code into a class

import pathlib
import json
import sys
from dataclasses import dataclass
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


@dataclass
class BroadcastData:
    """Represents relevant data for a broadcast.

    Attributes:
        broadcast_id: ID of broadcast. Required for youtube live API calls.
        broadcast_description: Description of the broadcast
        scheduled_start_time: Scheduled start time of stream. Required for youtube live API calls.
    """
    broadcast_id: str
    broadcast_description: str
    scheduled_start_time: str


def get_youtube_credentials(token_path: pathlib.Path) -> Credentials:
    assert token_path.exists(), (
        f'The provided path for api token is invalid: {token_path}'
    )

    scopes = [
        # get broadcast data
        'https://www.googleapis.com/auth/youtube.readonly',
        # modify broadcast description
        'https://www.googleapis.com/auth/youtube.force-ssl',
    ]
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            token_path,
            scopes=scopes,
        )
    except json.decoder.JSONDecodeError:
        sys.exit(
            'Please obtain a OAuth client ID, '
            'rename it to token.json, and add it to same folder as script\n'
            'https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth-installed.md#creating-application-credentials'
        )

    # opens authorization URL and runs a server to multiple API calls can be made
    flow.run_local_server()

    return flow.credentials


def get_broadcast_data(credentials: Credentials) -> BroadcastData:
    """Gets relevant data from the latest broadcast.

    Args:
        credentials (Credentials): Credentials used for making youtube live API calls.

    Returns:
        BroadcastData: Data containing relevant information to make API call.
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

    return BroadcastData(
        latest_broadcast['id'],
        latest_broadcast['snippet']['description'],
        latest_broadcast['snippet']['publishedAt'],
    )


def update_broadcast_description(credentials: Credentials, broadcast_data: BroadcastData, new_description: str) -> None:
    """Updates broadcast description with new description.

    Args:
        credentials (Credentials): Credentials used for making youtube live API calls.
        broadcast_data (BroadcastData): Data containing relevant information to make API call.
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
    # todo commandline argument
    token_path = pathlib.Path('token.json')
    credentials = get_youtube_credentials(token_path)
    broadcast_data = get_broadcast_data(credentials)
    update_broadcast_description(
        credentials,
        broadcast_data,
        f'{broadcast_data.broadcast_description} IT WORKED AGAIN',
    )


if __name__ == "__main__":
    main()
