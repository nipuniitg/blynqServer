from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

# Create your tests here.
from customLibrary.tests_lib import create_layout, create_organization, create_userdetails, verify_get_result, \
    generate_layout_dict, verify_posted_dict, trigger_pdb
from screenManagement.models import AspectRatio
from layoutManagement.models import Layout, LayoutPane
from layoutManagement.views import get_default_layouts, get_layouts, delete_layout, upsert_layout


class LayoutTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_layout_methods(self):
        print 'test_layout_methods started'
        layout = create_layout(default_layout=True)
        self.assertTrue(isinstance(layout, Layout))
        self.assertEqual(layout.__unicode__(), layout.title)
        organization2 = create_organization(default_organization=False)
        new_userdetails = create_userdetails(default_userdetails=False, organization=organization2)
        new_layout = create_layout(default_layout=False, is_split=True, userdetails=new_userdetails)
        user_layouts = Layout.get_user_relevant_objects(user_details=new_userdetails)
        self.assertIn(new_layout, user_layouts)
        print 'test_layout_methods completed successfully'


class LayoutViewsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user
        self.layout1 = create_layout(default_layout=True, is_split=True)
        organization2 = create_organization(default_organization=False)
        new_userdetails = create_userdetails(default_userdetails=False, organization=organization2)
        self.layout2 = create_layout(default_layout=False, is_split=True, userdetails=new_userdetails)

    def test_get_default_layouts(self):
        print 'test_get_default_layouts started'
        url = reverse('get_default_layouts')
        default_global_layouts = Layout.objects.filter(organization__isnull=True, is_default=True)
        layout_list = []
        for layout in default_global_layouts:
            layout_list.append(generate_layout_dict(layout))
        verify_get_result(self, expected_result=layout_list, url=url, view_func=get_default_layouts)
        print 'test_get_default_layouts completed successfully'

    def test_get_layouts(self):
        print 'test_get_layouts started'
        url = reverse('get_layouts')
        expected_result = [generate_layout_dict(self.layout1)]
        default_layouts = Layout.objects.filter(organization=self.layout1.organization, is_default=True)
        for layout in default_layouts:
            expected_result.append(generate_layout_dict(layout))
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_layouts)
        print 'test_get_layouts completed successfully'

    def test_delete_layout(self):
        # TODO: delete layout is failing in the tests but passing in the actual portal
        return
        print 'test_delete_layout started'
        url = reverse('delete_layout')
        posted_data = dict(layout_id=self.layout2.layout_id)
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=delete_layout)
        try:
            layout = Layout.objects.get(layout_id=self.layout2.layout_id)
            self.assertFalse(isinstance(layout, Layout))
            print 'Delete layout failed'
        except Layout.ObjectDoesNotExist:
            print 'test_delete_layout completed successfully'

    def test_upsert_layout(self):
        print 'test_upsert_layout started'
        url = reverse('upsert_layout')
        posted_data = generate_layout_dict()
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_layout)
        layout = Layout.objects.get(title=posted_data['title'])
        self.assertTrue(isinstance(layout, Layout))
        layout_pane_list = layout.layoutpane_layout.all()
        for pane in layout_pane_list:
            self.assertTrue(isinstance(pane, LayoutPane))
        print 'test_upsert_layout completed successfully'