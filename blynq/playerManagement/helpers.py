from copy import deepcopy
from itertools import chain
from operator import itemgetter

from customLibrary.custom_settings import CONTENT_ORGANIZATION_NAME
from customLibrary.views_lib import debugFileLog, mail_exception
from layoutManagement.serializers import default_layout_pane_serializer
from playlistManagement.serializers import PlaylistSerializer
from screenManagement.models import ORIENTATION_CHOICES
from screenManagement.serializers import AspectRatioSerializer


def schedule_pane_from_occurrence(occur):
    return occur.event.schedulepane_event


def is_conflicting(cur_occur, new_occur):
    """
    :param cur_occur: this event occurrence has more priority
    :param new_occur: this event occurrence has less priority
    :return: True if both the occurrences have the same schedule_pane and cur_occur overlaps with occur, else False
    """
    try:
        cur_schedule_pane = schedule_pane_from_occurrence(cur_occur)
        new_schedule_pane = schedule_pane_from_occurrence(new_occur)
        if cur_schedule_pane.schedule_id == new_schedule_pane.schedule_id:
            # Two occurrences of the same schedule can never conflict
            return False
        elif cur_schedule_pane.schedule.layout_id == new_schedule_pane.schedule.layout_id and \
                        cur_schedule_pane.layout_pane_id != new_schedule_pane.layout_pane_id:
            # Two occurrences from same layout and different layout_pane_id can never conflict
            return False
        elif (cur_occur.start <= new_occur.start <= cur_occur.end) or (new_occur.start <= cur_occur.start <= new_occur.end):
            return True
    except Exception as e:
        mail_exception(exception=e)
    return False


def merge_occurrence(existing_occurrences, new_occur):
    """
    :param new_occur: new event occurrence which has low priority compared to event occurrences in existing_occurrences
    :param existing_occurrences: the list of event occurrences computed till now
    :return: modified existing_occurrences based on the start_time and end_time of the new occurrence
    """
    # Merge the new occur into existing_occurrences
    # two occurrences are overlapping only if layout_pane_id is same and time period overlaps
    new_occur_parts = []
    for cur_occur in existing_occurrences:
        if is_conflicting(cur_occur, new_occur):
            # compare start times with < and end times with >
            if new_occur.start < cur_occur.start:
                if new_occur.end <= cur_occur.end:
                    new_occur.end = cur_occur.start
                else:
                    new_occur_part = deepcopy(new_occur)
                    new_occur.end = cur_occur.start
                    new_occur_part.start = cur_occur.end
                    new_occur_parts.append(new_occur_part)
            else:
                if new_occur.end <= cur_occur.end:
                    # new_occur lies in between cur_occur
                    new_occur = None
                    break
                else:
                    new_occur.start = cur_occur.end
    if new_occur:
        existing_occurrences.append(new_occur)
    for each_new_occur_part in new_occur_parts:
        existing_occurrences = merge_occurrence(existing_occurrences, each_new_occur_part)
    return existing_occurrences


def event_json_from_occurrences(existing_occurrences):
    screen_data_json = []
    for occur in existing_occurrences:
        schedule_pane = schedule_pane_from_occurrence(occur)
        schedule = schedule_pane.schedule
        # User added playlists in a pane should be appear after each playlist in Content Partner
        content_partner_playlists = schedule_pane.playlists.filter(organization__organization_name=CONTENT_ORGANIZATION_NAME)
        user_added_playlists = schedule_pane.playlists.exclude(organization__organization_name=CONTENT_ORGANIZATION_NAME)
        all_playlists = list(chain(user_added_playlists))
        for each_partner_playlist in content_partner_playlists:
            all_playlists = list(chain(all_playlists, [each_partner_playlist], user_added_playlists))
        # all_playlists = schedule_pane.playlists.all()
        playlists_json = PlaylistSerializer().serialize(all_playlists, fields=('playlist_id', 'playlist_title',
                                                                               'playlist_items'))
        aspect_ratio_list = [schedule.layout.aspect_ratio] if schedule.layout and schedule.layout.aspect_ratio else []
        aspect_ratio = AspectRatioSerializer().serialize(aspect_ratio_list)
        orientation = aspect_ratio[0]['orientation'] if aspect_ratio else ORIENTATION_CHOICES[0][0]
        layout_pane_dict = default_layout_pane_serializer([schedule_pane.layout_pane])[0]
        layout_pane_dict['orientation'] = orientation
        campaign_dict = {'schedule_id': schedule.schedule_id,
                         'playlists': playlists_json,
                         'pane': layout_pane_dict,
                         'mute_audio': schedule_pane.mute_audio,
                         'randomize_playlist_items': False,
                         'last_updated_time': schedule.last_updated_time,
                         'start_time': occur.start,
                         'end_time': occur.end}
        screen_data_json.append(campaign_dict)
    sorted_screen_data = sorted(screen_data_json, key=itemgetter('start_time'))
    return sorted_screen_data


def screen_schedule_data(schedule_panes, start_time, end_time):
    """
    :param schedule_panes: schedule_panes should be sorted descending by last_updated_time of the schedule
    :param start_time: start_time of the time interval to calculate event occurrences
    :param end_time: end_time of the time interval to calculate event occurrences
    :return: schedule data of non-overlapping event occurrences
    """
    existing_occurrences = []
    for obj in schedule_panes:
        if obj.event:
            event_occurrences = obj.event.get_occurrences(start_time, end_time)
            # existing_occurrences.update(event_occurrences)
            # Comment below two lines and uncomment above line if merging is to be removed
            for new_occur in event_occurrences:
                existing_occurrences = merge_occurrence(existing_occurrences, new_occur)
    return event_json_from_occurrences(existing_occurrences)