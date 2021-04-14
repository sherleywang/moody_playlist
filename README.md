# Project Outline

Last Updated: April 14, 2021
### Project Description
A Python 3 project that takes a music library and classifies the songs (mp3 files) into certain moods, creating playlists with these moods.

### Step 0: Set Up Environment
Follow the instructions given in [this](setup.md) README.

### Step 1: Tagging Data
Take a variety of songs (mp3 files) and determine which mood they best represent. This will be the labeling of the training and development data.
#### A. Determine moods to use
Some moods to consider:  
*Epic* - heroic and powerful sounding, songs you would play during a battle scene  
*Lighthearted* - somewhat cheerful and happy sounding, songs that uplift spirits or give off an overall positive vibe  
*Energetic* - exciting, songs that can give people a rush of adrenaline and hype up the dance floor  
*Calm* - peaceful and serene music, songs to listen to when one is trying to sleep or meditate  
*Chill* - rhythmical, music with a contemporary R&B feel and songs between energetic and calm  
*Miscellaneous* - songs that are a mix of multiple moods or mood is ambiguous  
These considerations may change depending on the tagging process of songs.  
#### B. Determine songs to use
A good number is around 750 to 1000 songs. These chosen songs should vary in terms of genre, lyrics, instrumentals, and fluctuation in mood (songs that can be interpreted as multiple moods).
#### C. Label the songs
Label each song with an integer representing the mood. Store the mapping of songs to moods as a CSV file named [mood_data.csv](data/mood_data.csv) in the data folder. This is the mapping of integers to moods:  
**1**: epic  
**2**: lighthearted  
**3**: energetic  
**4**: calm  
**5**: chill  
**6**: miscellaneous

### Step 2: Feature Extraction
Determine features to use for the classifier. This process is done so the model can classify a new and unseen song just by having the mp3 file.
#### A. Explore packages for feature extraction
The following packages were used in feature extraction:  
[pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis/) audio feature extraction, segmentation  
[LibROSA](https://github.com/librosa/librosa) has common features of audio and music analysis  
#### B. Determine and extract features
Four sets of features were extracted from this dataset.  
1. Basic Features (5 features)  
2. Engineered Features (28 features)  
3. pyAudioAnalysis Neural Network Features (136 features)  
4. Raw WAV File Features (100,000 features)  

#### C. Store features to avoid timely feature extraction
The feature extraction process first checks for existing CSV files to determine which mp3 files already have valid features. Then, using the command line, a text file of all mp3 files that need to have features extracted is generated. Using this file, the feature extraction code will only operate on the files listed. In the end, the newly-created features are added to the end of the existing features CSV files. This process is built-in the feature extraction code located [here](music/feature_extraction.ipynb).  

### Step 3: Training and Testing the Model
#### A. Train several classifiers using scikit-learn
Trained classifiers:  
1. Support Vector Machine  
2. Logistic Regression  
3. K Nearest Neighbor  
4. Gaussian Naive Bayes  
5. Random Forest  
6. Multi-Layer Perceptron (using pyAudioAnalysis features)  
7. Multi-Layer Perceptron (using raw digital signal)  

#### B. Ensemble the trained classifiers into one model
A stacked classifier was trained using the first 5 classifiers. Then, a weighted formula was used to combine the predictions of the stacked classifier with the two perceptron models to generate a final prediction. 

### Step 4: Combining into Application
Create an application with the trained model as the classifier. This application takes in mp3 files and classifies each song into a mood category. In the end, the application will output a playlist for each mood category.
#### A. Figure out how to export the trained model
Code a way to export the model so we don't have to retrain it every time the application runs.
#### B. Explore packages for creating playlists
The following packages may help in creating playlists:  
[MMPython](https://sourceforge.net/projects/mmpython/) retrieves metadata from mp3  
[ID3](http://id3-py.sourceforge.net/) read and manipulate id3 informational tags for mp3 files  
[PyID3](https://github.com/myers/pyid3) pure Python library for reading and writing id3 tags  
[beets](http://beets.io/) has tools for creating playlists and managing music library  
#### C. Build the application
Write a program that takes in mp3 files, uses the classifier, and then outputs one playlist per mood category.
