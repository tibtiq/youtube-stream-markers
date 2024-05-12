"""This module interacts with youtube's api to update a livestream's description."""

import json
import logging
import pathlib
import pickle
import sys
from dataclasses import dataclass

import google.auth.exceptions
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# todo turn this code into a class


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


def get_youtube_credentials_from_file(youtube_credentials_path: pathlib.Path) -> Credentials:
    """Get youtube credentials from file.

    Args:
        youtube_credentials_path: Path to saved youtube credentials.

    Returns:
        Credentials used to make Youtube API calls.
    """
    with open(youtube_credentials_path, 'rb') as file:
        youtube_credentials = pickle.load(file)

    # ! untested
    if youtube_credentials.expired:
        youtube_credentials.refresh(Request())

    return youtube_credentials


def get_youtube_credentials_from_oauth(oauth_credentials_path: pathlib.Path) -> Credentials:
    """Get youtube credentials from oauth credentials.

    After getting youtube credentials they will be saved for reuse.

    Args:
        oauth_credentials_path: Path to oauth credentials.

    Returns:
        Credentials used to make Youtube API calls.
    """
    assert oauth_credentials_path.exists(), (
        f'The provided path for api credentials is invalid: {oauth_credentials_path}'
    )

    scopes = [
        # get broadcast data
        'https://www.googleapis.com/auth/youtube.readonly',
        # modify broadcast description
        'https://www.googleapis.com/auth/youtube.force-ssl',
    ]
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            oauth_credentials_path,
            scopes=scopes,
        )
    except json.decoder.JSONDecodeError:
        sys.exit(
            'Please obtain a OAuth client ID\n'
            'https://github.com/googleapis/google-api-python-client/blob/main/docs/'
            'oauth-installed.md#creating-application-credentials'
        )

    # opens authorization URL and runs a server to multiple API calls can be made
    flow.run_local_server()
    youtube_credentials = flow.credentials

    youtube_credentials_path = pathlib.Path(__file__).parent.parent / '.config'
    youtube_credentials_path.mkdir(parents=True, exist_ok=True)
    with open(youtube_credentials_path / 'youtube_credentials.dat', 'wb') as file:
        pickle.dump(youtube_credentials, file)

    return flow.credentials


def get_youtube_credentials(oauth_credentials_path: pathlib.Path) -> Credentials:
    """Get youtube credentials with given Oauth credentials.

    Args:
        credentials_path (pathlib.Path): Path to OAuth credentials for youtube API credentials.

    Returns:
        Credentials: Google OAuth credentials that can be reused with Flow API calls.
    """
    youtube_credentials_path = pathlib.Path(
        __file__
    ).parent.parent / '.config' / 'youtube_credentials.dat'
    youtube_credentials = None
    try:
        logging.debug('loading youtube credentials from file')
        raise google.auth.exceptions.RefreshError
        # youtube_credentials = get_youtube_credentials_from_file(youtube_credentials_path)
    except google.auth.exceptions.RefreshError:
        logging.debug('loading youtube credentials from oauth')
        youtube_credentials = get_youtube_credentials_from_oauth(oauth_credentials_path)

    return youtube_credentials


def get_broadcast_data(credentials: Credentials) -> BroadcastData:
    """Get relevant data from the latest broadcast.

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


def update_broadcast_description(
    credentials: Credentials,
    broadcast_data: BroadcastData,
    new_description: str
) -> None:
    """Update broadcast description with new description.

    Args:
        credentials (Credentials): Credentials used for making youtube live API calls.
        broadcast_data (BroadcastData): Data containing relevant information to make API call.
        new_description (str): Text to replace broadcast's current description.
    """
    with build('youtube', 'v3', credentials=credentials) as service:
        # pylint: disable=no-member
        _ = service.liveBroadcasts().update(
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
    """Entry point to script when run directly."""
    # todo commandline argument
    token_path = pathlib.Path('credentials.json')
    credentials = get_youtube_credentials(token_path)
    broadcast_data = get_broadcast_data(credentials)
    update_broadcast_description(
        credentials,
        broadcast_data,
        f'{broadcast_data.broadcast_description} IT WORKED AGAIN',
    )


if __name__ == "__main__":
    main()
