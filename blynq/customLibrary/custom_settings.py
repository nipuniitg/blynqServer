from blynq.settings import DEBUG

# Don't change the below name if you aren't sure.
CONTENT_ORGANIZATION_NAME = 'Partner Content'

PLAYER_UPDATES_DIR = 'player_updates'
PLAYER_LOG_DIR = 'player_logs'

PLAYER_POLL_TIME = 65  # Time difference in seconds between successive polls of the player
PLAYER_INACTIVE_THRESHOLD = PLAYER_POLL_TIME + 1    # Wait this time (in seconds) to change status of screen as inactive

PLAYER_NOTIFY_MAIL = ['jaydev@blynq.in']

WIDGET_SCROLL_TIME = 180

COMPRESS_IMAGE = False

PERMANENTLY_DELETE_FILES = True

CONTENT_THUMBNAILS = {
    'pdf': '/static/images/pdf_logo.png',
    'image': '/static/images/image_icon.png',
    'video': '/static/images/video_icon.png',
    'folder': '/static/images/folder_icon.png',
    'url': '/static/images/url_icon.png',
    'audio': '/static/images/audio_icon.png',
    'rss': '/static/images/rss_icon.png',
    'fb':'/static/images/fb_icon.png',
    'instagram' : '/static/images/instagram_icon.png'
}

#INSTAGRAM 
if DEBUG:
    INSTAGRAM_CLIENTID = 'ff65285a12b34085bbaad2cf17d95ac2'
    CLIENT_SECRET = 'e118c806016d44a5a47b0381ed0e0b0b'
    REDIRECT_URI = 'http://127.0.0.1:8000/authentication/instagramRedirect'
else:
    INSTAGRAM_CLIENTID = '124dcb38dcfd4230b7ab7ac19d0fec15'
    CLIENT_SECRET = '450ed60a56ff47079a26271b08c132e8'
    REDIRECT_URI = 'http://www.blynq.in/authentication/instagramRedirect'