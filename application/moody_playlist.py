#!/usr/bin/env python

# import music analysis packages
import librosa
import pyAudioAnalysis as pyaudio
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import MidTermFeatures

# import tkinter package utility
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Button
from tkinter.ttk import Progressbar

# import other packages
import os
import copy
import time
import ntpath
import pickle
import warnings
import numpy as np
import pandas as pd

# initialize a tkinter object to select the directory with MP3 files
tkobj = tkinter.Tk()
tkobj.withdraw()
tkobj.directory = filedialog.askdirectory(message = "Select the folder containing the MP3 files.")

# path is the global variable for the folder chosen
path = tkobj.directory
tkobj.destroy()

# initialize the progress bar
tkobj2 = tkinter.Tk()
tkobj2.title("Moody Playlist")
progress = Progressbar(tkobj2, length = 300, mode = 'determinate')

# ignore warnings generated from audioread for loading MP3 files
warnings.filterwarnings('ignore')

'''
FUNCTIONALITY main loop for analyzing music for mood and generating playlists
'''
def music_analysis():
    # disable the button so program doesn't restart on click
    button.configure(state = "disabled")
    
    start = time.time()

    # start the progress bar
    progress['value'] = 10
    tkobj2.update()

    m3u_paths, librosa_feats, pyaudio_feats, feat_names = extract_features()
    # show an error message if feature extraction failed
    if len(pyaudio_feats) != len(librosa_feats):
        messagebox.showinfo("Error", "MP3 files failed to import. Please restart the program.")
    eng_features, nn_features = format_features(librosa_feats, pyaudio_feats, feat_names)
    predictions = load_models_and_predict(eng_features, nn_features)
    generate_playlists(predictions, eng_features, m3u_paths)

    end = time.time()

    # display time elapsed and success message
    time_elapsed = round((end - start) / 60, 2)
    message = "Total Time Elapsed: " + str(time_elapsed) + " minutes"
    messagebox.showinfo("Playlists have been successfully created.", message)
    tkobj2.update()
    tkobj2.destroy()

'''
FUNCTIONALITY extract raw features using packages librosa and pyAudioAnalysis
RETURN m3u_paths: paths to each song, librosa_feats: features from librosa, pyaudio_feats: features
from pyAudioAnalysis, feat_names: names of features
'''
def extract_features():
    # initialize feature data structures
    m3u_paths = {}
    librosa_feats = {}
    pyaudio_feats = {}
    feat_names = None

    # variables for pyAudioAnalysis feature extraction
    mid_term_window = 1
    mid_term_step = 1
    short_term_window = 0.05
    short_term_step = 0.05

    for root, dirs, files in os.walk(path, topdown = False):
        # extract features from the root directory chosen
        pyaudio_feat, song_files, feat_names = MidTermFeatures.directory_feature_extraction(root, 
            mid_term_window, mid_term_step, short_term_window, short_term_step, False)
        
        # update the progress bar
        progress['value'] = 30
        tkobj2.update()

        index = 0
        for s in song_files:
            # save features as dictionary with song names as keys and pyAudioAnalysis features as values
            s_dict_name = ntpath.basename(s)
            if pyaudio_feat.ndim == 1:
                # special case of indexing when there is only one song
                pyaudio_feats[s_dict_name] = pyaudio_feat
            else:
                pyaudio_feats[s_dict_name] = pyaudio_feat[index]
            index += 1

        for folder in dirs:
            # extract pyaudioanalysis features from each subfolder
            folder_path = os.path.join(root, folder)
            pyaudio_feat, song_files, feat_names = MidTermFeatures.directory_feature_extraction(folder_path, 
                mid_term_window, mid_term_step, short_term_window, short_term_step, False)
            
            index = 0
            for s in song_files:
                # save features as dictionary with song names as keys and pyAudioAnalysis features as values
                s_dict_name = ntpath.basename(s)
                if pyaudio_feat.ndim == 1:
                    # special case of indexing when there is only one song
                    pyaudio_feats[s_dict_name] = pyaudio_feat
                else:
                    pyaudio_feats[s_dict_name] = pyaudio_feat[index]
                index += 1

        # go through all mp3 files to extract librosa features
        for song in files:
            song_path = os.path.join(root, song)
            if song_path.endswith(".mp3"):
                # get the tempo of the song
                waveform, samp_rate = librosa.load(song_path)
                tempo, beat_frames = librosa.beat.beat_track(waveform, samp_rate)

                # get the chroma number of the song
                beat_times = librosa.frames_to_time(beat_frames, samp_rate)
                y_harmonic, y_percussive = librosa.effects.hpss(waveform)
                chromagram = librosa.feature.chroma_cqt(y_harmonic, samp_rate)
                beat_chroma = librosa.util.sync(chromagram, beat_frames, aggregate = np.median)
                
                # calculate the diff of beat chroma to convert information into a single float
                chroma_df = pd.DataFrame(beat_chroma)
                diff_values = chroma_df.diff()
                diff_mean = diff_values.mean(axis = 0, skipna = True)
                chroma_num = sum(diff_mean) / len(diff_mean)
                
                # save the librosa features and the full path of each mp3 song
                librosa_feats[song] = [tempo, chroma_num]
                m3u_paths[song] = song_path
        
    # update the progress bar
    progress['value'] = 75
    tkobj2.update()

    return (m3u_paths, librosa_feats, pyaudio_feats, feat_names)

'''
FUNCTIONALITY convert raw features into two feature DataFrames (engineered features and neural network features)
PARAMETERS librosa_feats: librosa features, pyaudio_feats: pyAudioAnalysis features, feat_names: names of features
RETURN eng_features: engineered features (selected pyAudioAnalysis features + librosa features),
nn_features: neural network features (all pyAudioAnalysis features)
'''
def format_features(librosa_feats, pyaudio_feats, feat_names):
    # only keep desired features from pyAudioAnalysis for stacking classifier
    new_pyaudio_feats = {}
    selected_feats = ['zcr_mean', 'zcr_std', 'energy_mean', 'energy_entropy_mean', 'spectral_centroid_mean', 
                        'spectral_spread_mean', 'spectral_entropy_mean', 'mfcc_2_mean', 'mfcc_5_mean', 'mfcc_6_mean',
                        'spectral_centroid_std', 'spectral_entropy_std', 'spectral_spread_std', 'chroma_7_std',
                        'delta chroma_2_std', 'delta chroma_3_std', 'delta chroma_9_std', 'delta chroma_std_std',
                        'delta energy_std', 'delta mfcc_1_std', 'delta mfcc_3_std', 'delta mfcc_13_std',
                        'delta spectral_centroid_std', 'delta spectral_entropy_std', 'delta spectral_flux_std',
                        'delta spectral_spread_std']
    # save selected features into the dictionary new_pyaudio_feats
    for key, value in pyaudio_feats.items():
        index_list = [feat_names.index(feat) for feat in selected_feats]
        extracted_feats = [value[i] for i in index_list]
        new_pyaudio_feats[key] = extracted_feats
    
    # combine selected pyAudioAnalysis features with librosa features for engineered features
    librosa_df = pd.DataFrame(librosa_feats)
    librosa_df = librosa_df.transpose()
    eng_pyaudio_df = pd.DataFrame(new_pyaudio_feats)
    eng_pyaudio_df = eng_pyaudio_df.transpose()
    eng_features = librosa_df.merge(eng_pyaudio_df, right_index = True, left_index = True)
    eng_features.sort_index(inplace = True)

    # generate neural network features (raw pyAudioAnalysis features)
    pyaudio_df = pd.DataFrame(pyaudio_feats)
    pyaudio_df = pyaudio_df.transpose()
    nn_features = pyaudio_df
    nn_features.sort_index(inplace = True)

    # update the progress bar
    progress['value'] = 85
    tkobj2.update()

    return (eng_features, nn_features)

'''
FUNCTIONALITY use previously trained models to predict the moods based on extracted features
PARAMETERS eng_features: engineered features, nn_features: neural network features (for MLP)
RETURN final_preds: predictions combined from the stacking classifier and MLP model
'''
def load_models_and_predict(eng_features, nn_features):
    # use the stacking classifier
    loaded_stacker = pickle.load(open('mood_stacking_model.sav', 'rb'))
    stacker_preds = loaded_stacker.predict(eng_features)
    # use the MLP classifier
    loaded_mlp = pickle.load(open('mood_mlp_model.sav', 'rb'))
    mlp_preds = loaded_mlp.predict(nn_features)
    
    # combine the predictions from both models to generate final predictions
    final_preds = []
    for i in range(len(stacker_preds)):
        stack_pred = stacker_preds[i]
        mlp_pred = mlp_preds[i]
        
        if stack_pred != mlp_pred:
            # prediction was different between stacking and mlp models
            if stack_pred == 1 or stack_pred == 3:
                # prefer stacking classifier for moods 1 and 3
                final_preds.append(stack_pred)
            else:
                final_preds.append(mlp_pred)
        else:
            # predictions are the same, just append mlp's prediction
            final_preds.append(mlp_pred)
    
    # update the progress bar
    progress['value'] = 95
    tkobj2.update()

    return final_preds

'''
FUNCTIONALITY generate playlists (m3u files) based on mood
PARAMETERS predictions: mood predictions for each song from models, eng_features: engineered features,
m3u_paths: dictionary of paths to each song
'''
def generate_playlists(predictions, eng_features, m3u_paths):
    # generate song lists based on predicted moods
    # mood key: 1 epic, 2 lighthearted, 3 energetic, 4 calm, 5 chill, 6 miscellaneous
    epic = []
    lighthearted = []
    energetic = []
    calm = []
    chill = []
    miscellaneous = []

    # ordering of indices are the same as engineered features due to prior sorting
    for i in range(len(predictions)):
        song = eng_features.index[i]
        pred = predictions[i]
        if pred == 1:
            epic.append(song)
        if pred == 2:
            lighthearted.append(song)
        if pred == 3:
            energetic.append(song)
        if pred == 4:
            calm.append(song)
        if pred == 5:
            chill.append(song)
        if pred == 6:
            miscellaneous.append(song)

    # get relative paths for each song for m3u file writing
    m3u_paths_relative = {}
    for key, value in m3u_paths.items():
        root_length = len(path) + 1
        m3u_paths_relative[key] = value[root_length:]
    
    # create the playlist files
    write_playlist("epic_playlist", epic, m3u_paths_relative)
    write_playlist("lighthearted_playlist", lighthearted, m3u_paths_relative)
    write_playlist("energetic_playlist", energetic, m3u_paths_relative)
    write_playlist("calm_playlist", calm, m3u_paths_relative)
    write_playlist("chill_playlist", chill, m3u_paths_relative)
    write_playlist("miscellaneous_playlist", miscellaneous, m3u_paths_relative)

    # update the progress bar
    progress['value'] = 100
    tkobj2.update()

'''
FUNCTIONALITY writes a m3u file based on a list of songs (all of the same mood)
PARAMETERS filename: name of the playlist, mood_list: list of songs in a particular mood,
m3u_paths_relative: dictionary with relative paths of each song
'''
def write_playlist(filename, mood_list, m3u_paths_relative):
    full_path = path + "/" + filename + ".m3u"
    file = open(full_path, "w")
    playlist = [m3u_paths_relative[song] + "\n" for song in mood_list]
    # add the header for the m3u file
    playlist.insert(0, "#EXTM3U\n")
    file.writelines(playlist)
    file.close()

# create a button that on press will start the program
progress.pack(padx = 50, ipady = 20)
button = Button(tkobj2, text = 'Generate Playlists', command = music_analysis)
button.pack(padx = 50, ipady = 20)
tkobj2.mainloop()