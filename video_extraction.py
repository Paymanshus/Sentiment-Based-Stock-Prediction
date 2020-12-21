# Getting the video
# Getting frames from video
# OCR on frames(separate file?)
# Video to Audio
# SpeechRecognition(transcription) on audio from video
# Saving everything
#     Frames from video to folder
#     OCR and save images with their text in a csv file(indexed with [file_name, caption, date])])
#     Audio transcription as CSV(indexed as [file_name, captioning])


import pandas as pd
import numpy as np
import cv2
import os
import glob
import moviepy.editor as mp
import matplotlib.pyplot as plt
import csv
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


def create_dirs(vid_name):

    vid_name = (os.path.splitext(vid_name)[0])
    vid_dir = f'{frames_dir}/{vid_name}_frames'

    if not os.path.exists(vid_dir):
        os.makedirs(vid_dir)

    return vid_dir


def frames_extract(vid_name):

    vid = cv2.VideoCapture(vid_loc)

    # create directory to save frames
    vid_dir = create_dirs(vid_name)

    currentframe = 0
    framename = 0

    while(True):

        ret, frame = vid.read()

        if ret:

            if currentframe % 100 == 0:
                name = vid_dir + '/' + str(framename) + '.jpg'
                print('Saving: ' + name)

                # writing the extracted images
                cv2.imwrite(name, frame)

                framename += 1

            currentframe += 1

        else:
            break

    vid.release()
    cv2.destroyAllWindows()


def audio_extract(vid_name):

    clip = mp.VideoFileClip(vids_dir + '/' + vid_name + '.mp4')

    audio_loc = f'{audios_dir}/{vid_name}.wav'

    clip.audio.write_audiofile(audio_loc)

    return audio_loc


# # Unused, replaced by silence_based_conversion()
# def speech_recognition(vid_loc):

#     vid_name = os.path.basename(vid_loc)
#     vid_name = os.path.splitext(vid_name)[0]

#     # Get audio from video clip if not already present in audios folder
#     if f'{vid_name}.wav' not in os.listdir(audios_dir):
#         print('Creating audio clip')
#         audio_loc = audio_extract(vid_loc)

#     else:
#         audio_loc = f'{audios_dir}/{vid_name}.wav'

#     r = sr.Recognizer()
#     r.pause_threshold = 1
#     audio = sr.AudioFile(audio_loc)

#     with audio as source:
#         r.adjust_for_ambient_noise(source)
#         audio = r.record(source)
#     transcription = r.recognize_google(audio)
#     print(transcription)


def silence_based_conversion(vid_loc):

    vid_name = os.path.basename(vid_loc)
    vid_name = os.path.splitext(vid_name)[0]
    print(vid_name + '------------------------------------------------------------------')
    print(audios_dir)
    # Get audio from video clip if not already present in audios folder
    if f'{vid_name}.wav' not in os.listdir(audios_dir):
        print('Creating audio clip')
        audio_loc = audio_extract(vid_name)

    else:
        audio_loc = f'{audios_dir}/{vid_name}.wav'

    # open the audio file stored in
    # the local system as a wav file.
    audio = AudioSegment.from_wav(audio_loc)
    print(audio.dBFS)

    # open a file where we will concatenate
    # and store the recognized text
    fh = open(f"{transcriptions_dir}/{vid_name}.txt", "w+")

    # split track where silence is 0.5 seconds
    # or more and get chunks
    chunks = split_on_silence(audio,
                              min_silence_len=600,
                              silence_thresh=-50
                              )

    # create a directory to store the audio chunks.
    vid_chunks = f'{chunks_dir}/{vid_name}_chunks'
    flag = 0

    try:
        os.mkdir(vid_chunks)

    except(FileExistsError):
        flag = 1

    i = 0
    # process each chunk
    for chunk in chunks:
        print(i)
        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(duration=20)

        # add 0.5 sec silence to beginning and
        # end of audio chunk. This is done so that
        # it doesn't seem abruptly sliced.
        audio_chunk = chunk_silent + chunk + chunk_silent

        # export audio chunk and save it in
        # the current directory.
        print("saving chunk{0}.wav".format(i))
        # specify the bitrate to be 192 k
        audio_chunk.export(f"{vid_chunks}/chunk{i}.wav",
                           bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = vid_chunks + '/chunk'+str(i)+'.wav'

        print("Processing chunk "+str(i))

        # SPEECH RECOGNITION - SEPARATE INTO METHOD
        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = True
            r.energy_threshold = 50

            audio_listened = r.listen(source)

        try:
            rec = r.recognize_google(audio_listened)
            # write the output to the file.
            fh.write(rec+". ")

        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1


if __name__ == "__main__":

    # Globals
    vids_dir = 'Videos'
    frames_dir = 'Frames'
    audios_dir = 'Audios'
    transcriptions_dir = 'Text'
    chunks_dir = 'Chunks'

    # Hard coded for testing purposes, would use os.walk to select video name otherwise and concatenate vids_dir
    vid_loc = 'Videos/papajohn.mp4'
    vid_name_ext = 'papajohn.mp4'

    # vid_name = os.path.basename(vid_loc)
    # vid_name = os.path.splitext(vid_name)[0]
    vid_name = 'papajohn'

    # frames_extract(vid_name)

    # silence_based_conversion(vid_loc)

    for video in os.listdir(vids_dir):
        if(video.endswith(".mp4")):
            silence_based_conversion(vids_dir + '/' + video)

    # for audio in os.listdir(audios_dir):
    #     print(audio)
