import os
from blynq.settings import MEDIA_ROOT, MEDIA_URL, HOST_URL
from customLibrary.views_lib import debugFileLog

__author__ = 'nipun'
from authentication.models import Organization
from reports.models import ScreenAnalytics
import csv


# To generate monthly reports for an organization
def organization_monthly(organization_name="Remedo"):
    try:
        org = Organization.objects.filter(organization_name=organization_name)[0]
        sc_data = ScreenAnalytics.objects.filter( screen__owned_by=org ).values_list("screen__screen_name", "session_start_time", "session_end_time" )
        filename = organization_name + "_monthly.csv"
        reports_rel_path = os.path.join("reports", filename)
        file_url = HOST_URL + MEDIA_URL + reports_rel_path
        full_filename = os.path.join(MEDIA_ROOT, reports_rel_path)
        f = open(full_filename, 'wb')
        writer = csv.writer(f, delimiter=",")
        new_all_data = {}
        for data in sc_data:
            key = (data[0], str(data[1].year), str(data[1].month))
            if key not in new_all_data:
                new_all_data[ key ] = 0
            new_all_data[key] += (data[2] - data[1]).seconds

        for key in new_all_data:
            row = []
            row.append(key[0])
            row.append(key[1])
            row.append(key[2])
            seconds = new_all_data[key]
            min, sec = divmod( seconds, 60)
            hr, min = divmod( min, 60)
            active_time = "%d hrs %d mins %d seconds" % ( hr, min, sec )
            row.append(str(active_time))
            writer.writerow(row)
        f.close()
    except Exception as e:
        file_url = "Error occurred, please contact support@blynq.in "
        debugFileLog.exception("Error generating report for " + str(organization_name) + str(e))
    return file_url
