# Don't change the below name if you aren't sure.
CONTENT_ORGANIZATION_NAME = 'Partner Content'

PLAYER_UPDATES_DIR = 'player_updates'
PLAYER_LOG_DIR = 'player_logs'

PLAYER_POLL_TIME = 120  # Time difference in seconds between successive polls of the player
PLAYER_INACTIVE_THRESHOLD = PLAYER_POLL_TIME + 1    # Wait this time (in seconds) to change status of screen as inactive

COMPRESS_IMAGE = True

PERMANENTLY_DELETE_FILES = True

CONTENT_THUMBNAILS = {
    'pdf': '/static/images/pdf_logo.png',
    'video': '/static/images/video_icon.png',
    'folder': '/static/images/folder_icon.png',
    'url': '/static/images/url_icon.png',
    'audio': '/static/images/audio_icon.png',
    'rss': '/static/images/rss_icon.png'
}
