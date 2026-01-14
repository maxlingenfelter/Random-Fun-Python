"""
Panopto Transcript Fetcher

Fetches transcripts/captions from Panopto videos using the REST API.
Requires OAuth2 authentication with your Panopto instance.

Usage:
    1. Set up API credentials in your Panopto admin panel
    2. Configure the variables below or use environment variables
    3. Run: python panopto_transcript.py <video_id>

Example:
    python panopto_transcript.py 31dde761-45e1-48cb-9f79-b3b0014b48de
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin, urlparse, parse_qs


class PanoptoClient:
    """Client for interacting with Panopto REST API."""

    def __init__(self, server: str, client_id: str, client_secret: str, username: str = None, password: str = None):
        """
        Initialize the Panopto client.

        Args:
            server: Panopto server URL (e.g., 'ncsu.hosted.panopto.com')
            client_id: OAuth2 client ID from Panopto admin
            client_secret: OAuth2 client secret from Panopto admin
            username: (Optional) Username for resource owner grant
            password: (Optional) Password for resource owner grant
        """
        self.server = server.rstrip('/')
        if not self.server.startswith('http'):
            self.server = f'https://{self.server}'

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.session = requests.Session()

    def _get_auth_url(self) -> str:
        """Get the OAuth2 token endpoint URL."""
        return f'{self.server}/Panopto/oauth2/connect/token'

    def _get_api_url(self, endpoint: str) -> str:
        """Get full API URL for an endpoint."""
        return f'{self.server}/Panopto/api/v1/{endpoint.lstrip("/")}'

    def authenticate(self) -> bool:
        """
        Authenticate with Panopto using OAuth2.

        Tries resource owner password grant if credentials provided,
        otherwise uses client credentials grant.

        Returns:
            True if authentication successful, False otherwise.
        """
        auth_url = self._get_auth_url()

        if self.username and self.password:
            # Resource Owner Password Grant (user-specific access)
            data = {
                'grant_type': 'password',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.username,
                'password': self.password,
                'scope': 'api'
            }
        else:
            # Client Credentials Grant (app-level access)
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'api'
            }

        try:
            response = self.session.post(auth_url, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data.get('access_token')

            if self.access_token:
                self.session.headers['Authorization'] = f'Bearer {self.access_token}'
                print(f"Successfully authenticated with {self.server}")
                return True
            else:
                print("Error: No access token in response")
                return False

        except requests.exceptions.HTTPError as e:
            print(f"Authentication failed: {e}")
            if e.response is not None:
                print(f"Response: {e.response.text}")
            return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def get_session(self, session_id: str) -> dict:
        """
        Get session (video) details by ID.

        Args:
            session_id: The Panopto session GUID

        Returns:
            Session data dict including caption download URL if available.
        """
        url = self._get_api_url(f'sessions/{session_id}')

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Failed to get session: {e}")
            if e.response is not None:
                print(f"Response: {e.response.text}")
            return None

    def get_caption_download_url(self, session_id: str) -> str:
        """
        Get the caption download URL for a session.

        Args:
            session_id: The Panopto session GUID

        Returns:
            URL to download captions, or None if not available.
        """
        session_data = self.get_session(session_id)

        if not session_data:
            return None

        # The API returns caption URL in various possible fields
        caption_url = (
            session_data.get('CaptionDownloadUrl') or
            session_data.get('captionDownloadUrl') or
            session_data.get('Captions') or
            session_data.get('captions')
        )

        if caption_url:
            return caption_url

        # Print available fields for debugging
        print("\nSession data fields:")
        for key, value in session_data.items():
            if 'caption' in key.lower() or 'transcript' in key.lower():
                print(f"  {key}: {value}")

        return None

    def download_captions(self, session_id: str, output_file: str = None, format: str = 'vtt') -> str:
        """
        Download captions for a session.

        Args:
            session_id: The Panopto session GUID
            output_file: Path to save captions (optional)
            format: Caption format - 'vtt' or 'srt' (default: vtt)

        Returns:
            Caption text content, or None if download failed.
        """
        caption_url = self.get_caption_download_url(session_id)

        if not caption_url:
            print("No caption URL found for this session.")
            print("The video may not have captions, or you may not have access.")
            return None

        # Ensure full URL
        if not caption_url.startswith('http'):
            caption_url = f'{self.server}{caption_url}'

        try:
            response = self.session.get(caption_url)
            response.raise_for_status()

            caption_text = response.text

            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(caption_text)
                print(f"Captions saved to: {output_file}")

            return caption_text

        except requests.exceptions.HTTPError as e:
            print(f"Failed to download captions: {e}")
            return None

    def search_sessions(self, query: str, max_results: int = 25) -> list:
        """
        Search for sessions containing the query in captions, name, or description.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of matching session dicts.
        """
        url = self._get_api_url('sessions/search')
        params = {
            'searchQuery': query,
            'pageNumber': 0,
            'pageSize': max_results
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('Results', [])
        except requests.exceptions.HTTPError as e:
            print(f"Search failed: {e}")
            return []


def extract_video_id(url_or_id: str) -> str:
    """
    Extract video ID from a Panopto URL or return as-is if already an ID.

    Args:
        url_or_id: Either a full Panopto URL or just the session ID

    Returns:
        The session ID (GUID)
    """
    if '/' in url_or_id or '?' in url_or_id:
        # It's a URL, extract the ID
        parsed = urlparse(url_or_id)
        params = parse_qs(parsed.query)
        if 'id' in params:
            return params['id'][0]
    return url_or_id


def main():
    # Configuration - set these via environment variables or edit directly
    PANOPTO_SERVER = os.environ.get('PANOPTO_SERVER', 'ncsu.hosted.panopto.com')
    CLIENT_ID = os.environ.get('PANOPTO_CLIENT_ID', '')
    CLIENT_SECRET = os.environ.get('PANOPTO_CLIENT_SECRET', '')
    USERNAME = os.environ.get('PANOPTO_USERNAME', '')  # Optional
    PASSWORD = os.environ.get('PANOPTO_PASSWORD', '')  # Optional

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python panopto_transcript.py <video_url_or_id>")
        print("\nRequired environment variables:")
        print("  PANOPTO_SERVER      - Your Panopto server (e.g., ncsu.hosted.panopto.com)")
        print("  PANOPTO_CLIENT_ID   - OAuth2 client ID")
        print("  PANOPTO_CLIENT_SECRET - OAuth2 client secret")
        print("\nOptional environment variables:")
        print("  PANOPTO_USERNAME    - Your Panopto username")
        print("  PANOPTO_PASSWORD    - Your Panopto password")
        sys.exit(1)

    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: PANOPTO_CLIENT_ID and PANOPTO_CLIENT_SECRET must be set.")
        print("\nTo get API credentials:")
        print("1. Log into Panopto as an admin")
        print("2. Go to System > Identity Providers")
        print("3. Click 'Create API Client'")
        print("4. Set the grant type and copy the credentials")
        sys.exit(1)

    video_input = sys.argv[1]
    video_id = extract_video_id(video_input)
    print(f"Video ID: {video_id}")

    # Create client and authenticate
    client = PanoptoClient(
        server=PANOPTO_SERVER,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME if USERNAME else None,
        password=PASSWORD if PASSWORD else None
    )

    if not client.authenticate():
        print("\nFailed to authenticate. Check your credentials.")
        sys.exit(1)

    # Get session info
    print(f"\nFetching session info...")
    session_data = client.get_session(video_id)

    if session_data:
        print(f"\nSession: {session_data.get('Name', 'Unknown')}")
        print(f"Duration: {session_data.get('Duration', 'Unknown')} seconds")
        print(f"Folder: {session_data.get('FolderName', 'Unknown')}")

    # Download captions
    print(f"\nDownloading captions...")
    output_file = f"{video_id}_captions.vtt"
    captions = client.download_captions(video_id, output_file=output_file)

    if captions:
        print(f"\n--- Caption Preview (first 500 chars) ---")
        print(captions[:500])
        print("...")
    else:
        print("\nNo captions available for this video.")


if __name__ == '__main__':
    main()
