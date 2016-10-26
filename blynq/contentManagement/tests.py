from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.test.client import MULTIPART_CONTENT
from contentManagement.models import Content
from contentManagement.views import delete_content, create_folder, move_content, folder_path, get_files_json, \
    get_folders_json, update_content_title, upload_content
from customLibrary.tests_lib import create_content, create_userdetails, create_organization, verify_posted_dict, \
    verify_get_result, generate_content_dict

# Create your tests here.


class ContentTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_content_methods(self):
        content = create_content(default_content=True, is_folder=False)
        self.assertTrue(isinstance(content, Content))
        self.assertEqual(content.__unicode__(), content.title)
        self.assertEqual(content.natural_key(), content.title)
        self.assertEqual(content.logical_path(), '/')
        self.assertEqual(content.logical_path_list(), [{'content_id': content.content_id, 'title': content.title}])
        # Create a file in some other organization and verify that get_user_relevant_objects works fine
        organization2 = create_organization(default_organization=False)
        new_userdetails = create_userdetails(default_userdetails=False, organization=organization2)
        content2 = create_content(default_content=False, is_folder=False, userdetails=new_userdetails)
        user_content = Content.get_user_relevant_objects(user_details=new_userdetails)
        self.assertEqual(list(user_content), list([content2]))
        content.delete()
        content2.delete()
        # TODO: Add a test case for verifying the organization file storage limit

    def test_folder_methods(self):
        # Create a folder and verify
        parent_folder = create_content(default_content=True, is_folder=True)
        self.assertTrue(isinstance(parent_folder, Content))
        self.assertEqual(parent_folder.content_type, None)
        self.assertEqual(parent_folder.__unicode__(), parent_folder.title)
        self.assertEqual(parent_folder.natural_key(), parent_folder.title)
        self.assertEqual(parent_folder.logical_path(), '/')
        parent_folder_list = [{'content_id': parent_folder.content_id, 'title': parent_folder.title}]
        self.assertEqual(parent_folder.logical_path_list(), parent_folder_list)
        # Create a child folder inside parent folder and verify
        child_folder = create_content(default_content=False, is_folder=True, parent_folder=parent_folder)
        self.assertEqual(child_folder.logical_path(), '/'+parent_folder.title+'/')
        parent_folder_list.append({'content_id': child_folder.content_id, 'title': child_folder.title})
        child_folder_list = parent_folder_list
        self.assertEqual(child_folder.logical_path_list(), child_folder_list)
        parent_folder.delete()


class ContentViewsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user

    def test_folder_path(self):
        parent_folder = create_content(default_content=False, is_folder=True)
        content1 = create_content(default_content=True, is_folder=False, parent_folder=parent_folder)
        folder1 = create_content(default_content=True, is_folder=True, parent_folder=parent_folder)
        url = reverse('folder_path', kwargs={'current_folder_id': parent_folder.content_id})
        expected_result = [{'content_id': -1, 'title': 'Home'}]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=folder_path,
                          current_folder_id=-1)
        expected_result.append({'content_id': parent_folder.content_id, 'title': parent_folder.title})
        verify_get_result(self, expected_result=expected_result, url=url, view_func=folder_path,
                          current_folder_id=parent_folder.content_id)
        expected_result.append({'content_id': folder1.content_id, 'title': folder1.title})
        verify_get_result(self, expected_result=expected_result, url=url, view_func=folder_path,
                          current_folder_id=folder1.content_id)
        content1.delete()
        folder1.delete()
        print 'test_folder_path completed successfully'

    def test_get_files_json(self):
        parent_folder = create_content(default_content=True)
        content1 = create_content(default_content=True, is_folder=False)
        content2 = create_content(default_content=False, is_folder=False)
        url = reverse('get_files_json', kwargs={'parent_folder_id': -1})
        expected_result = [generate_content_dict(content1), generate_content_dict(content2)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_files_json,
                          parent_folder_id=-1)
        content1.parent_folder = parent_folder
        content1.save()
        content2.parent_folder = parent_folder
        content2.save()
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_files_json,
                          parent_folder_id=parent_folder.content_id)
        content1.delete()
        content2.delete()
        print 'test_get_files_json completed successfully'

    def test_get_folders_json(self):
        folder1 = create_content(default_content=True, is_folder=True)
        folder2 = create_content(default_content=False, is_folder=True)
        url = reverse('get_folders_json', kwargs={'parent_folder_id': -1})
        expected_result = [generate_content_dict(folder1), generate_content_dict(folder2)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_folders_json,
                          parent_folder_id=-1)
        parent_folder = create_content(default_content=True)
        folder1.parent_folder = parent_folder
        folder1.save()
        folder2.parent_folder = parent_folder
        folder2.save()
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_folders_json,
                          parent_folder_id=parent_folder.content_id)
        print 'test_get_folders_json completed successfully'

    def test_delete_content(self):
        url = reverse('delete_item')
        content1 = create_content(default_content=True, is_folder=False)
        content2 = create_content(default_content=False, is_folder=False)
        content3 = create_content(default_content=True, is_folder=True)
        posted_data = {'content_ids': [content1.content_id, content2.content_id, content3.content_id]}
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=delete_content)
        print 'test_delete_content completed successfully'

    def test_create_folder(self):
        url = reverse('create_folder')
        folder1 = create_content(default_content=True, is_folder=True)
        title = 'test create folder'
        posted_data = dict(currentFolderId=folder1.content_id, title=title)
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=create_folder)
        folder2 = Content.objects.get(title=title)
        self.assertEqual(folder2.parent_folder.content_id, folder1.content_id,
                         msg='Incorrect create of folder inside some other folder')
        folder1.delete()
        folder2.delete()
        print 'test_create_folder completed successfully'

    def test_move_content(self):
        url = reverse('move_content')
        parent_folder = create_content(default_content=True, is_folder=True)
        content1 = create_content(default_content=True, is_folder=False)
        folder1 = create_content(default_content=False, is_folder=True)
        posted_data = dict(content_ids=[content1.content_id, folder1.content_id],
                           parent_folder_id=parent_folder.content_id)
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=move_content)
        content1 = Content.objects.get(content_id=content1.content_id)
        folder1 = Content.objects.get(content_id=folder1.content_id)
        self.assertEqual(content1.parent_folder, parent_folder)
        self.assertEqual(folder1.parent_folder, parent_folder)
        folder1.delete()
        content1.delete()
        print 'test_move_content completed successfully'

    def test_update_content_title(self):
        url = reverse('update_content_title')
        content1 = create_content(default_content=True)
        new_title = 'test update content title'
        posted_data = dict(content_id=content1.content_id, title=new_title)
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=update_content_title)
        content = Content.objects.get(content_id=content1.content_id)
        self.assertEqual(content.title, new_title)
        content1.delete()
        print 'test_update_content_title completed successfully'

    def test_upload_content(self):
        url = reverse('upload_content')
        new_file1 = SimpleUploadedFile("test image1.jpg", "file_content", content_type="image/jpeg")
        new_file2 = SimpleUploadedFile("test image2.jpg", "file_content", content_type="image/jpeg")
        posted_data = dict(totalFiles=2, currentFolderId=-1, file0=new_file1, file1=new_file2)
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upload_content,
                           content_type=MULTIPART_CONTENT)
        content1 = Content.objects.get(title='test image1')
        content2 = Content.objects.get(title='test image2')
        self.assertTrue(isinstance(content1, Content))
        self.assertTrue(isinstance(content2, Content))
        content1.delete()
        content2.delete()
        print 'test_upload_content completed successfully'
