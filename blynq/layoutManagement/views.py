from django.db import transaction

from customLibrary.views_lib import obj_to_json_response, get_userdetails, string_to_dict, debugFileLog, ajax_response, \
    mail_exception
from layoutManagement.models import Layout, LayoutPane
from layoutManagement.serializers import default_layout_serializer

# Create your views here.


def get_layouts(request):
    """
    :param request:
    :return: the user relevant Layouts created in the organization.
    """
    user_details = get_userdetails(request)
    query_set = Layout.get_user_relevant_objects(user_details=user_details)
    json_data = default_layout_serializer(query_set)
    return obj_to_json_response(json_data)


def get_default_layouts(request):
    """
    :param request:
    :return: the default layouts which are common to all the organizations like Full Screen
    """
    query_set = Layout.objects.filter(organization__isnull=True, is_default=True)
    json_data = default_layout_serializer(query_set)
    return obj_to_json_response(json_data)


@transaction.atomic
def upsert_layout(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    layout_schedules = []
    try:
        with transaction.atomic():
            layout_id = int(posted_data.get('layout_id'))
            title = posted_data.get('title')
            aspect_ratio = posted_data.get('aspect_ratio')
            aspect_ratio_id = aspect_ratio.get('aspect_ratio_id')
            layout_panes = posted_data.get('layout_panes')
            if layout_id == -1:
                layout = Layout(title=title, aspect_ratio_id=aspect_ratio_id, created_by=user_details,
                                last_updated_by=user_details, organization=user_details.organization)
                layout_created = True
            else:
                layout = Layout.get_user_relevant_objects(user_details).get(layout_id=layout_id)
                layout.title = title
                layout.aspect_ratio_id = aspect_ratio_id
                layout_created = False
                layout.last_updated_by = user_details
                from scheduleManagement.models import Schedule
                layout_schedules = Schedule.get_user_relevant_objects(user_details).filter(layout=layout)
            layout.save()
            layout_id = layout.layout_id
            layout_pane_id_list = []
            for each_layout_pane in layout_panes:
                layout_pane_id = int(each_layout_pane.get('layout_pane_id'))
                title = each_layout_pane.get('title')
                left_margin = int(each_layout_pane.get('left_margin'))
                top_margin = int(each_layout_pane.get('top_margin'))
                z_index = int(each_layout_pane.get('z_index'))
                width = int(each_layout_pane.get('width'))
                height = int(each_layout_pane.get('height'))
                if layout_pane_id == -1:
                    layout_pane = LayoutPane(title=title, left_margin=left_margin, top_margin=top_margin,
                                             z_index=z_index, width=width, height=height, layout_id=layout_id)
                    layout_pane.save()
                    layout_pane_id = layout_pane.layout_pane_id
                    each_layout_pane['layout_pane_id'] = layout_pane_id
                    if not layout_created:
                        # Add an entry in SchedulePane corresponding to this newly created layout pane
                        from scheduleManagement.models import SchedulePane
                        for each_schedule in layout_schedules:
                            SchedulePane.objects.create(schedule=each_schedule, layout_pane_id=layout_pane_id)
                else:
                    LayoutPane.objects.filter(layout_pane_id=layout_pane_id).update(
                        title=title, left_margin=left_margin, top_margin=top_margin, z_index=z_index, width=width,
                        height=height, layout_id=layout_id)
                layout_pane_id_list.append(layout_pane_id)
            # Remove the remaining layout_pane which are not in layout_pane_id_list
            layout_panes = LayoutPane.objects.filter(layout_id=layout_id).exclude(layout_pane_id__in=layout_pane_id_list)
            if layout_panes:
                layout_panes.delete()
            posted_data['layout_id'] = layout_id
            success = True
    except Exception as e:
        mail_exception(exception=e)
        errors = ['Error while creating the layout']
    return ajax_response(success=success, errors=errors, obj_dict={'saved_layout': posted_data})


@transaction.atomic
def delete_layout(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    layout_id = int(posted_data.get('layout_id'))
    success = False
    errors = []
    try:
        layout = Layout.get_user_relevant_objects(user_details).get(layout_id=layout_id)
        with transaction.atomic():
            layout.delete()
            success = True
    except Exception as e:
        mail_exception(exception=e)
        errors = ['Error while deleting the layout, Layout is already in use']
    return ajax_response(success=success, errors=errors)
