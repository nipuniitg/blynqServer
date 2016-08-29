from subprocess import Popen, PIPE
from datetime import datetime
import subprocess
import os
import time
import csv

"""
Script to download content from youtube channels of partners
"""


print "Starting script .."

terminate_text = "upload date is not in range"
current_date = datetime.today().strftime('%Y%m%d')


def download_videos(file_row):
    category = file_row[0]
    channel_url = row[1]
    commandToExecute = "youtube-dl -f \'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio\'" + \
                       " --merge-output-format mp4 --dateafter now-2day " + \
                       "-o  " + "'" + current_date + "/" + category + "/" + "%(uploader)s/" + \
                       "%(title)s-%(id)s.%(ext)s" + "' " + channel_url
    print commandToExecute
    process = Popen(commandToExecute,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    return process


def monitor_logs(process):
    while process.poll() is None:
        log_line = process.stdout.readline()
        print log_line
        if terminate_text in log_line:
            print "Killing process .."
            process.kill()
            return
    return


current_dir = os.path.dirname(__file__)
path_to_file = "channels.csv"
print current_dir

file_path = os.path.join(current_dir, path_to_file)
f = open(file_path, 'rb')
reader = csv.reader(f)

for row in reader:
    print "Downloading from url " + row[1]
    process = download_videos(row)
    monitor_logs(process)
    print "Stopped further download from " + row[1]

f.close()




