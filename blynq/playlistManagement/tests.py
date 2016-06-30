from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

# Create your tests here.
from blynq.settings import MEDIA_HOST
from customLibrary.tests_lib import create_playlist, create_playlist_items, create_userdetails, create_organization, \
    verify_get_result, generate_content_dict, create_content, verify_posted_dict, generate_playlist_dict, \
    generate_playlist_item_dict
from playlistManagement.models import Playlist, PlaylistItems
from playlistManagement.views import get_playlists, get_files_recursively_json, upsert_playlist, delete_playlist


class PlaylistTest(TestCase):
    def test_playlist(self):
        playlist = create_playlist(default_playlist=True)
        self.assertTrue(isinstance(playlist, Playlist))
        self.assertEqual(playlist.__unicode__(), playlist.playlist_title)
        new_organization = create_organization(default_organization=False)
        new_userdetails = create_userdetails(default_userdetails=False, organization=new_organization)
        playlist2 = create_playlist(default_playlist=False, userdetails=new_userdetails)
        user_playlists = Playlist.get_user_relevant_objects(user_details=new_userdetails)
        self.assertEqual(list(user_playlists), list([playlist2]))

    def test_playlist_items(self):
        playlist_item = create_playlist_items(default_playlist_item=True, position_index=1)
        self.assertTrue(isinstance(playlist_item, PlaylistItems))
        unicode_str = playlist_item.playlist.playlist_title + ' - ' + playlist_item.content.title
        self.assertEqual(playlist_item.__unicode__(), unicode_str)
        playlist_item.content.delete()


class PlaylistViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user

    def test_get_playlists(self):
        url = reverse('get_playlists')
        playlist1 = create_playlist(default_playlist=True)
        playlist_item1 = create_playlist_items(default_playlist_item=False, playlist=playlist1)
        playlist_item2 = create_playlist_items(default_playlist_item=False, playlist=playlist1)
        playlist2 = create_playlist(default_playlist=False)
        expected_result = [generate_playlist_dict(playlist1), generate_playlist_dict(playlist2)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_playlists)
        playlist_item1.content.delete()
        playlist_item2.content.delete()
        print 'test_get_playlists completed successfully'

    def test_get_files_recursively_json(self):
        url = reverse('get_files_recursively', kwargs={'parent_folder_id': -1})
        content1 = create_content(default_content=True, is_folder=False)
        folder1 = create_content(default_content=True, is_folder=True)
        content2 = create_content(default_content=False, is_folder=False, parent_folder=folder1)
        expected_result = [generate_content_dict(content1, include_is_folder=False),
                           generate_content_dict(content2, include_is_folder=False)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_files_recursively_json,
                          parent_folder_id=-1)
        content1.delete()
        content2.delete()
        print 'test_get_files_recursively_json completed successfully'

    def test_upsert_playlist(self):
        url = reverse('upsert_playlist')
        content1 = create_content(default_content=True, is_folder=False)
        folder1 = create_content(default_content=True, is_folder=True)
        content2 = create_content(default_content=False, is_folder=False, parent_folder=folder1)
        playlist_title = 'test upsert playlist'
        posted_data = dict(playlist_id=-1, playlist_title=playlist_title, playlist_items=[])
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_playlist)
        playlist = Playlist.objects.get(playlist_title=playlist_title)
        self.assertTrue(isinstance(playlist, Playlist))
        # Now change playlist title and verify
        new_playlist_title = 'changed playlist title'
        posted_data = dict(playlist_id=playlist.playlist_id, playlist_title=new_playlist_title,
                           playlist_items=[generate_playlist_item_dict(content=content1),
                                           generate_playlist_item_dict(content=content2)])
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_playlist)
        playlist = Playlist.objects.get(playlist_id=playlist.playlist_id)
        self.assertTrue(isinstance(playlist, Playlist))
        self.assertEqual(playlist.playlist_title, new_playlist_title)
        playlist_items = playlist.playlistitems_set.all().values_list('content_id', flat=True)
        self.assertItemsEqual([content1.content_id, content2.content_id], playlist_items)
        # Now change the display time of a playlist item and check whether it is updated
        new_display_time = 40
        posted_data['playlist_items'][0]['display_time'] = new_display_time
        modified_content_id = posted_data['playlist_items'][0]['content_id']
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_playlist)
        playlist_item = PlaylistItems.objects.get(playlist_id=playlist.playlist_id, content_id=modified_content_id)
        self.assertEqual(playlist_item.display_time, new_display_time)
        content1.delete()
        content2.delete()
        print 'test_upsert_playlist completed successfully'

    def test_delete_playlist(self):
        url = reverse('delete_playlist')
        playlist = create_playlist(default_playlist=True)
        playlist_item = create_playlist_items(default_playlist_item=True, playlist=playlist)
        posted_data = dict(playlist_id=playlist.playlist_id)
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=delete_playlist)
        content = playlist_item.content
        try:
            playlist = Playlist.objects.get(playlist_id=playlist.playlist_id)
            self.assertTrue(False, msg='delete_playlist failed as playlist exists')
        except Exception as e:
            try:
                playlist_item = PlaylistItems.objects.get(playlist_item_id=playlist_item.playlist_item_id)
                self.assertTrue(False, msg='delete_playlist failed as playlist item exists')
            except Exception as e:
                content.delete()
                print 'test_delete_playlist completed successfully'