# Project Outline

Last Updated: May 7, 2021

### Project Description
A Python 3 project that takes a music library and classifies the songs into certain moods, creating playlists using these moods.
The program takes a directory and analyzes all MP3 files within that directory and its subdirectories. Using two pre-trained
models (a stacking classifier and a multi-layer perceptron model), the program classifies all songs into one of six moods: epic,
lighthearted, energetic, calm, chill or miscellaneous. Finally, six M3U files (playlists) are generated using the moods and exported 
into the same directory as the MP3 files.  

### Application Usage
To use the application without any modifications, follow the instructions given in this [tutorial](setup.md).  
*Although this application utilizes the command line to run, it has a simple GUI for easy access.*

### Workflow Step 0: Setting Up the Environment
Use Anaconda as the base environment for developing the program. To properly set up the Anaconda environment, follow the
instructions in the Environment Setup section of [this](setup.md#Environment_Setup) README.

### Workflow Step 1: Tagging Data
Take a variety of songs (MP3 files) and determine which mood they best represent. These songs will be the labeled data used for training 
supervised learning models.

#### A. Moods
All songs will be categorized into one of the following six moods:  
1. *Epic* - heroic and powerful sounding, songs you would play during a battle scene  
2. *Lighthearted* - somewhat cheerful and happy sounding, songs that give off an overall positive vibe but are not overwhelming  
3. *Energetic* - exciting sounding songs that can give a rush of adrenaline, music used to hype up the dance floor  
4. *Calm* - peaceful and serene music, songs to listen to when one is trying to sleep or meditate  
5. *Chill* - rhythmical music with a contemporary R&B feel, songs that are balanced between energetic and calm  
6. *Miscellaneous* - songs with dramatic mood changes throughout or music where the mood is extremely ambiguous

#### B. Songs
200 songs (MP3 files) that varied in language, genre, lyrics, instrumentals, and fluctuation in mood were chosen from a list of my favorite songs.
Some statistics about the songs and plots of the data distribution of the moods can be found [here](data/data_distribution.md). The code for generating these statistics and plots can be found [here](data_overview.html).

#### C. Labeling
The chosen songs were labeled with a primary mood and a secondary mood based solely on my discretion. Songs that clearly only represented one mood were labeled that mood as the primary mood and miscellaneous as the secondary mood. Labeling was performed using integers as a map to the mood that the song represents. The labeled data is stored as a CSV file named [mood_data.csv](data/mood_data.csv) in the [data](data) folder. 
Here is the mapping of integers to moods:  

1 **-->** epic  
2 **-->** lighthearted  
3 **-->** energetic  
4 **-->** calm  
5 **-->** chill  
6 **-->** miscellaneous

### Workflow Step 2: Feature Extraction
Determine features to use for training the classifiers. These features will also be extracted whenever the application is classifying songs.

#### A. Packages for Feature Extraction
The following packages were used to extract features from the MP3 files:  
[pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis/) was used to obtain a wide variety of audio features such as zero crossing rate, energy, and MFCC  
[librosa](https://github.com/librosa/librosa) was used to obtain the tempo of each song and also the chromagram layered with the beat frames

#### B. Sets of Features
Three sets of features were extracted from this dataset for training. The feature extraction code can be found [here](music/feature_extraction.html).
1. Basic Features (5 features)  
    - The basic features include the tempo, chroma number, zero crossing rate, energy entropy, and spectral centroid of each song. These features are common audio features that are usually distinct between songs of different moods. It should be noted that I created the chroma number feature by converting the data from the beat-frame-layered chromagram into a float (details are in the feature extraction [code](music/feature_extraction.html)). Additionally, the correlation matrix of these features is plotted
    [here](data/data_distribution.md#Correlation_Matrix_of_5_Basic_Features).
2. Engineered Features (28 features)  
    - Feature selection was used to create the engineered features. The pyAudioAnalysis package generates 136 distinct features for each song. I plotted all data distributions of these features [here](data_overview.html) to determine the pyAudioAnalysis features with the greatest variation between primary moods. I selected 26 of these features to be the engineered features and included the two features (tempo and chroma number) generated from the librosa package for a total of 28 engineered features. Additionally, the correlation matrix of these features is plotted
    [here](data/data_distribution.md#Correlation_Matrix_of_28_Engineered_Features) and the data distributions for each of the chosen engineered features is plotted [here](data/data_distribution.md#Data_Distribution_Plots_of_Engineered_Features).
3. pyAudioAnalysis Neural Network Features (138 features)
    - All features extracted from both packages were used (136 features from pyAudioAnalysis and 2 features from librosa) for training the multi-layer perceptron model.

#### C. Storing Features to Save Time
Extracting features is expensive in terms of time. Therefore, the feature extraction process first checks for existing CSV files to determine which MP3 files already have valid features. Then, using the command line, a TXT file of all MP3 files that need to have features extracted is generated. The feature extraction code will use this file to only operate on the MP3 files missing features. In the end, the newly-created features are added to the end of the existing CSV files. This process is built-in the feature extraction [code](music/feature_extraction.html).

### Workflow Step 3: Training and Testing the Model
#### A. Train several classifiers using scikit-learn
Trained classifiers:  
1. Support Vector Machine  
2. Logistic Regression  
3. K Nearest Neighbor  
4. Gaussian Naive Bayes  
5. Random Forest  
6. Multi-Layer Perceptron 

#### B. Ensemble the trained classifiers into one model
A stacked classifier was trained using the first 5 classifiers. Then, a weighted formula was used to combine the predictions of the stacked classifier with the two perceptron models to generate a final prediction. 

### Workflow Step 4: Combining into Application
Create an application with the trained model as the classifier. This application takes in mp3 files and classifies each song into a mood category. In the end, the application will output a playlist for each mood category.
#### A. Figure out how to export the trained model
Code a way to export the model so we don't have to retrain it every time the application runs.
#### B. Explore packages for creating playlists

#### C. Build the application
Write a program that takes in mp3 files, uses the classifier, and then outputs one playlist per mood category.

### Workflow Step 5: Future Steps

### Known Issues
