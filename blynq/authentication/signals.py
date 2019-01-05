from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import Organization
from customLibrary.views_lib import debugFileLog, mail_exception


default_layout_list = [
    {"aspect_ratio": {"height_component": 9, "width_component": 16, "aspect_ratio_id": 3, "orientation": "LANDSCAPE", "title": "16:9 Landscape"},
     "layout_panes": [{"z_index": 0, "title": "Main-Pane", "top_margin": 0, "height": 75, "width": 100, "left_margin": 0},
                      {"z_index": 1, "title": "Bottom-Pane", "top_margin": 75, "height": 25, "width": 100, "left_margin": 0}],
     "title": "2-Pane(Horizontal-Split)"},

    {"aspect_ratio": {"height_component": 9, "width_component": 16, "aspect_ratio_id": 3, "orientation": "LANDSCAPE", "title": "16:9 Landscape"},
     "layout_panes": [{"z_index": 0, "title": "Main-Pane", "top_margin": 0, "height": 92, "width": 100, "left_margin": 0},
                      {"z_index": 1, "title": "Scroll", "top_margin": 92, "height": 8, "width": 100, "left_margin": 0}],
     "title": "1-Pane & Scroll"},

    {"aspect_ratio": {"height_component": 9, "width_component": 16, "aspect_ratio_id": 3, "orientation": "LANDSCAPE", "title": "16:9 Landscape"},
     "layout_panes": [{"z_index": 0, "title": "Main-Pane", "top_margin": 0, "height": 80, "width": 75, "left_margin": 0},
                      {"z_index": 1, "title": "Vertical-Pane", "top_margin": 0, "height": 80, "width": 25, "left_margin": 75},
                      {"z_index": 2, "title": "Bottom-Pane", "top_margin": 80, "height": 20, "width": 100, "left_margin": 0}],
     "title": "3-Pane(Type-1)"},

    {"aspect_ratio": {"height_component": 9, "width_component": 16, "aspect_ratio_id": 3, "orientation": "LANDSCAPE", "title": "16:9 Landscape"},
     "layout_panes": [{"z_index": 0, "title": "Main-Pane", "top_margin": 0, "height": 92, "width": 75, "left_margin": 0},
                      {"z_index": 1, "title": "Vertical-Pane", "top_margin": 0, "height": 92, "width": 25, "left_margin": 75},
                      {"z_index": 2, "title": "Scroll", "top_margin": 92, "height": 8, "width": 100, "left_margin": 0}],
     "title": "2-Pane  & Scroll"},

    {"aspect_ratio": {"height_component": 9, "width_component": 16, "aspect_ratio_id": 3, "orientation": "LANDSCAPE", "title": "16:9 Landscape"},
     "layout_panes": [{"z_index": 0, "title": "Main-Pane", "top_margin": 0, "height": 100, "width": 75, "left_margin": 0},
                      {"z_index": 1, "title": "Vertical-Pane", "top_margin": 0, "height": 100, "width": 25, "left_margin": 75}],
     "title": "2-Pane(Vertical-Split)"},

    {"aspect_ratio": {"height_component": 9, "width_component": 16, "aspect_ratio_id": 3, "orientation": "LANDSCAPE", "title": "16:9 Landscape"},
     "layout_panes": [{"z_index": 0, "title": "Main-Pane", "top_margin": 0, "height": 80, "width": 75, "left_margin": 0},
                      {"z_index": 1, "title": "Vertical-Pane", "top_margin": 0, "height": 100, "width": 25, "left_margin": 75},
                      {"z_index": 2, "title": "Bottom-Pane", "top_margin": 80, "height": 20, "width": 75, "left_margin": 0}],
     "title": "3-Pane(Type-2)"}]


def create_default_layouts(organization):
    try:
        from layoutManagement.models import Layout, LayoutPane
        organization_layouts = Layout.objects.filter(organization=organization, is_default=True)
        if organization_layouts.exists():
            return
        for layout in default_layout_list:
            title = layout.get('title')
            aspect_ratio_id = layout.get('aspect_ratio').get('aspect_ratio_id')
            try:
                new_layout = Layout(title=title, aspect_ratio_id=aspect_ratio_id, is_default=True, organization=organization)
                new_layout.save()
                layout_panes = layout.get('layout_panes')
                for each_pane in layout_panes:
                    each_pane['layout_id'] = new_layout.layout_id
                    new_pane = LayoutPane(**each_pane)
                    new_pane.save()
            except Exception as e:
                debugFileLog.exception(e)
    except Exception as e:
        debugFileLog.exception(e)
        mail_exception('Error while creating default layout for organization %s' % str(organization))


def update_total_screen_count(organization):
    try:
        screen_count = organization.get_screen_count()
        if screen_count > organization.total_screen_count:
            organization.total_screen_count = screen_count
            organization.save()
    except Exception as e:
        debugFileLog.exception(e)
        mail_exception('Error while updating the screen count of the organization %s' % str(organization))


def sync_users_active(organization):
    try:
        org_users = organization.get_users()
        for userdetails in org_users:
            if userdetails.user.is_active != organization.is_active:
                userdetails.user.is_active = organization.is_active
                userdetails.user.save()
    except Exception as e:
        debugFileLog.exception(e)


@receiver(post_save, sender=Organization)
def post_save_organization(sender, instance, **kwargs):
    debugFileLog.info("inside post_save_organization")
    create_default_layouts(instance)
    update_total_screen_count(instance)
    sync_users_active(instance)
