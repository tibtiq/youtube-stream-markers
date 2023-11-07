# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveBroadcasts.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from dataclasses import dataclass

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

CLIENT_SECRETS_FILE = 'token.json'
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@dataclass
class LivestreamData:
    livestream_id: str
    livestream_description: str
    scheduled_start_time: str

def get_livestream_data() -> LivestreamData:

    # Get credentials and create an API client
    scope = ['https://www.googleapis.com/auth/youtube.readonly']
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scope,
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        'youtube',
        'v3',
        credentials=credentials
    )

    request = youtube.liveBroadcasts().list(
        part='snippet',
        mine=True
    )
    response = request.execute()

    # get latest broadcast
    latest_broadcast = response['items'][0]

    return LivestreamData(
        latest_broadcast['id'],
        latest_broadcast['snippet']['description'],
        latest_broadcast['snippet']['publishedAt'],
    )

def update_description(livestream_data: LivestreamData, text_to_append: str) -> None:
    # Get credentials and create an API client
    scope = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scope,
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        'youtube',
        'v3',
        credentials=credentials
    )

    request = youtube.liveBroadcasts().update(
        part='snippet',
        body={
          'id': livestream_data.livestream_id,
          'snippet': {
            'scheduledStartTime': livestream_data.scheduled_start_time,
            'description': f'{livestream_data.livestream_description}\n{text_to_append}'
          }
        }
    )
    response = request.execute()

    print(response)

if __name__ == '__main__':
    livestream_data = get_livestream_data()

    update_description(livestream_data, '20:00 - ')