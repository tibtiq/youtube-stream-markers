from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from dataclasses import dataclass


@dataclass
class LivestreamData:
    """Represents relevant data for a livestream.

    Attributes:
        livestream_id: ID of livestream. Required for youtube live API calls.
        livestream_description: Description of the livestream
        scheduled_start_time: Scheduled start time of stream. Required for youtube live API calls.
    """
    livestream_id: str
    livestream_description: str
    scheduled_start_time: str


def get_livestream_data(credentials) -> LivestreamData:
    with build('youtube', 'v3', credentials=credentials) as service:
        response = service.liveBroadcasts().list(
            part='snippet',
            mine=True,
        ).execute()

    # get latest broadcast
    latest_broadcast = response['items'][0]

    return LivestreamData(
        latest_broadcast['id'],
        latest_broadcast['snippet']['description'],
        latest_broadcast['snippet']['publishedAt'],
    )


def update_livestream_description(credentials, livestream_data: LivestreamData, text_to_append: str) -> None:
    with build('youtube', 'v3', credentials=credentials) as service:
        response = service.liveBroadcasts().update(
            part='snippet',
            body={
                'id': livestream_data.livestream_id,
                'snippet': {
                    'scheduledStartTime': livestream_data.scheduled_start_time,
                    'description': f'{livestream_data.livestream_description}\n{text_to_append}'
                }
            }
        ).execute()


if __name__ == "__main__":
    import os

    SCOPES = [
        # get livestream data
        'https://www.googleapis.com/auth/youtube.readonly',
        # modify livestream description
        'https://www.googleapis.com/auth/youtube.force-ssl',
    ]
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

    livestream_data = get_livestream_data(credentials)
    print(livestream_data)
    update_livestream_description(
        credentials,
        livestream_data,
        'IT WORKED AGAIN',
    )
