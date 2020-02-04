from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
from moviepy.config import change_settings

import sys
import firebase_admin
from firebase_admin import credentials, firestore, storage
import datetime


# Download the file to a destination 
def download_to_local():
    downloadList = []
    cred = credentials.Certificate("video-concatenation-firebase-adminsdk-uz9e4-8356cd60ab.json")
    app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'video-concatenation.appspot.com',
    }, name='storage')

    bucket = storage.bucket(app=app)
    blobs=bucket.list_blobs(prefix="tempVideo/", delimiter="/") #List all objects that satisfy the filter.

    for blob in blobs:
        if len(blob.name.split("/")[1]) == 0:
            continue
        print("Download: " + blob.name)
        destination_uri = "{}".format(blob.name) 
        blob.download_to_filename(destination_uri)
        downloadList.append(destination_uri)
    return downloadList


def edit(downloadedFiles):

    clip1 = VideoFileClip(downloadedFiles[0]).fx(vfx.resize, width=WIDTH, height=HEIGHT)
    #text1 = TextClip(QUESTION_1, font="Amiri-Bold", fontsize=50, color="white",size=(WIDTH, HEIGHT)).set_pos("center").set_duration(3)
    textImage1 = ImageClip(QUESTION_1_PATH, duration=4)

    clip2 = VideoFileClip(downloadedFiles[1]).fx(vfx.resize, width=WIDTH, height=HEIGHT)
    textImage2 = ImageClip(QUESTION_2_PATH, duration=4)

    clip3 = VideoFileClip(downloadedFiles[2]).fx(vfx.resize, width=WIDTH, height=HEIGHT)
    textImage3 = ImageClip(QUESTION_3_PATH, duration=4)

    clip_end = VideoFileClip(CLIP_END_PATH).fx(vfx.resize, width=WIDTH, height=HEIGHT)

    final_clip = concatenate_videoclips([textImage1, clip1, textImage2, clip2, textImage3, clip3, clip_end], method="compose")

    # Add the Logo 
    logo = (ImageClip("braveTogetherLogo.png")
        .set_duration(final_clip.duration)
        .resize(height=80)
        .margin(right=8, top=8, opacity=0) # logo-border padding
        .set_pos(("right","top")))
    final = CompositeVideoClip([final_clip, logo])

    finalPath = downloadedFiles[0].replace("1", "-final")
    print(finalPath)
    final.write_videofile(finalPath)
    return finalPath

"""
Final clip on final_video/nitzolInteviwerDay-final.mp4
"""
if __name__ == "__main__":

    WIDTH = 720
    HEIGHT = 480

    QUESTION_1_PATH = "Question1.jpg"
    QUESTION_2_PATH = "Question2.jpg"
    QUESTION_3_PATH = "Question3.jpg"
    CLIP_END_PATH = "Clip_End.mp4"

    downloadedFiles = download_to_local()
    finalPath = edit(downloadedFiles)

    