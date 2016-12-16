from django.db.models import Sum
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from customLibrary.views_lib import debugFileLog, mail_exception
from playlistManagement.models import PlaylistItems, Playlist


@receiver(post_save, sender=PlaylistItems)
@receiver(post_delete, sender=PlaylistItems)
def playlist_items_changed(sender, instance, **kwargs):
    try:
        instance
    except Exception as e:
        debugFileLog.info('instance object does not exist in playlist_items_changed')
        return
    try:
        playlist_total_time = 0
        total_time = PlaylistItems.objects.filter(playlist_id=instance.playlist_id).aggregate(Sum('display_time'))
        if total_time['display_time__sum']:
            playlist_total_time = total_time['display_time__sum']
        # TODO: Scope for optimization : Change the below line to : "playlist = instance.playlist"
        playlist = Playlist.objects.get(playlist_id=instance.playlist_id)
        playlist.playlist_total_time = playlist_total_time
        playlist.save()
        if not playlist.user_visible and playlist.playlist_total_time == 0:
            playlist.delete()
    except Exception as e:
        debugFileLog.exception('Failed to update the playlist total time for playlist_id %d' % instance.playlist_id)
        mail_exception(exception=e)


@receiver(post_save, sender=Playlist)
@receiver(pre_delete, sender=Playlist)
def post_save_playlist(sender, instance, **kwargs):
    debugFileLog.info("Inside post_save_playlist of %s" % instance.playlist_title)
    # Set the last_updated_time for all the schedules having this playlist
    from scheduleManagement.models import SchedulePlaylists
    try:
        schedule_playlists = SchedulePlaylists.objects.filter(playlist_id=instance.playlist_id)
        for each_schedule_playlist in schedule_playlists:
            if each_schedule_playlist.schedule_pane:
                schedule = each_schedule_playlist.schedule_pane.schedule
                if schedule:
                    schedule.update_screens_data()
    except Exception as e:
        debugFileLog.exception("Error while updating the last_updated_time of the schedules "
                               "corresponding to playlist %s" % instance.playlist.playlist_title)
        mail_exception(exception=e)
