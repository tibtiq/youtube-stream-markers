# Options
Add stream markers to youtube VOD description after stream ends
Add stream markers to youtube VOD description as the markers are created


# Setup
## Setup
Create a Google Cloud Console project and now the project is selected

1. Enable YouTube Data API v3 in [Google Cloud console](https://console.cloud.google.com/apis/library)
2. Setup OAuth consent screen
    ### OAuth consent screen
    User Type
    - External
    App information
    - App name: NAME
    - User support email: Select the email associated with the project
    - Developer contact information: EMAIL
    ### Scopes
    - Add the following scopes:
    ```
    .../auth/youtube.force-ssl
    ```
    ### Test users
    Add the email of the YouTube channel you want to add stream markers to
3. Create OAuth 2.0 client [credentials](https://console.cloud.google.com/apis/credentials?)
    Create credentials -> OAuth client ID
    - Application type: Desktop app
    Download client secret as json


# Sources
- [Youtube Live Streaming API](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts)

    Documents available hooks with the API and allows testing them in the website

- [Python sample code for youtube Live Streaming API](https://github.com/youtube/api-samples/blob/master/python/README.md)