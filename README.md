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
instructions in the Environment Setup section of [this](setup.md#environment-setup) README.

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
    [here](data/data_distribution.md#correlation-matrix-of-5-basic-features).
2. Engineered Features (28 features)  
    - Feature selection was used to create the engineered features. The pyAudioAnalysis package generates 136 distinct features for each song. I plotted all data distributions of these features [here](data_overview.html) to determine the pyAudioAnalysis features with the greatest variation between primary moods. I selected 26 of these features to be the engineered features and included the two features (tempo and chroma number) generated from the librosa package for a total of 28 engineered features. Additionally, the correlation matrix of these features is plotted
    [here](data/data_distribution.md#correlation-matrix-of-28-engineered-features) and the data distributions for each of the chosen engineered features is plotted [here](data/data_distribution.md#data-distribution-plots-of-engineered-features).
3. pyAudioAnalysis Neural Network Features (138 features)
    - All features extracted from both packages were used (136 features from pyAudioAnalysis and 2 features from librosa) for training the multi-layer perceptron model.

#### C. Storing Features to Save Time
Extracting features is expensive in terms of time. Therefore, the feature extraction process first checks for existing CSV files to determine which MP3 files already have valid features. Then, using some Bash commands, a TXT file of all MP3 files that need to have features extracted is generated. The feature extraction code will use this file to only operate on the MP3 files missing features. In the end, the newly-created features are added to the end of the existing CSV files. If there are no existing feature CSV files, the feature extraction code will automatically generate them. This entire process is built-in the feature extraction [code](music/feature_extraction.html).

### Workflow Step 3: Training the Models
Train several supervised-learning classifier models on the dataset and export these models for use in the application.

#### A. Train Individual Classifiers
Using the package [Scikit-Learn](https://scikit-learn.org/stable/), basic features, engineered features and PCA-transformed engineered features were used to [train](models/training_models.html) several classifiers. The engineered features and PCA-transformed engineered features out-performed the basic features in all trained classifiers in terms of accuracy. Hence, it was determined that engineered features should be extracted and used for the application (PCA transformation is applied when it results in a higher accuracy). The pyAudioAnalysis neural network features were exclusively used to train the multi-layer perceptron model.  

A GridSearch cross validation pipeline was used to determine the best hyperparameters for each classifier.  

**Trained Classifiers with Best Hyperparameters:**
1. Support Vector Machine 
    - *C = 5, decision_function_shape = 'ovr', gamma = 0.1, kernel = 'sigmoid'*
2. Logistic Regression
    - *C = 0.25, penalty = 'l2', solver = 'liblinear'*
3. K Nearest Neighbor
    - *metric = 'chebyshev', n_neighbors = 9, weights = 'distance'*
4. Gaussian Naive Bayes
    - *var_smoothing = 1e-09*
5. Random Forest
    - *max_depth = None, max_features = 'log2', min_samples_leaf = 7*
6. Multi-Layer Perceptron
    - *activation = 'logistic', alpha = 0.1, hidden_layer_sizes = (60,), solver = 'adam'*

These classifiers provided accuracies ranging from 50% to 60%. The training code can be found [here](models/training_models.html).

#### B. Ensembling and Exporting
Due to the low accuracies from individual classifiers, a stacking classifier was [trained](models/training_models.html) using the first five trained classifiers with their respective best hyperparameters. The accuracy of this stacking classifier is between 60% and 70%. The stacking classifier and the multi-layer perceptron model were exported as [mood_stacking_model.sav](application/mood_stacking_model.sav) and [mood_mlp_model.sav](application/mood_mlp_model.sav) respectively. These models, located in the folder [application](application), are necessary for the application to run.

#### C. Prediction Function
A prediction function to generate one prediction based on predictions from the stacking classifier and the multi-layer perceptron model was created. This function prioritizes the stacking classifier whenever the stacking classifier predicts the mood to be epic or energetic. The function prioritizes the multi-layer perceptron model in all other cases. The creation of this function relied on an analysis of the precision and recall of both models for individual moods. The prediction function code can be found [here](application/moody_playlist.html).

### Workflow Step 4: Combining into Application
Create an application that takes a directory, scans it for all MP3 files, classifies each song based on mood, and outputs a playlist for each mood.

#### A. Build the GUI
The package [Tkinter](https://docs.python.org/3/library/tkinter.html) was used to create a simple GUI for the application. The interactive GUI shows up as soon as the Python modules for the application are loaded. This essentially means that after using Python to run the application on the command line, a user-friendly GUI will pop up shortly. The GUI consists of a folder selector, a button to start the application, a progress bar for status updates, and various message boxes for error and success messages. The GUI code can be found [here](application/moody_playlist.py). For more details about the GUI, the [tutorial](setup.md#using-the-application) includes pictures of all elements of the GUI.

#### B. Aggregate Code for Feature Extraction and Models
The feature extraction process was rewritten so that subdirectories can be scanned as well as the originally chosen directory. The rest of the workflow was converted into an application through the aggregation of all the code into [this](application/moody_playlist.py) file. This process made it so that to run the application, you only need the two trained model files and [this](application/moody_playlist.py) single Python file.

### Workflow Step 5: Future Steps
1. Rewrite the GUI part of the application using an alternative such as [PyGUI](https://www.cosc.canterbury.ac.nz/greg.ewing/python_gui/)
2. Export the application as a single executable under MacOS, Windows, and Linux
3. Tag more MP3 files to expand the dataset and retrain models for higher accuracy
4. Obtain computing resources to train more neural network models with raw features as the input

### Known Issues
1. Raw audio data was generated from the MP3 files through down sampling to create raw features. However, I did not have the computing resources to train neural networks with this huge input. The code for training models using raw features is located in the [deprecated](models/deprecated) folder. The following files can be used to train a multi-layer perceptron model with raw features: [large_models.html](models/deprecated/large_models.html), [neural_network_colab.html](models/deprecated/neural_network_colab.html). The code to extract raw features is located [here](music/deprecated/raw_feature_extraction.html).
    - Although I did manage to run parts of this code by constantly monitoring my Google Colab notebook, I was unable to run longer jobs with better hyperparameter choices to generate a trained model with higher than 30% accuracy.
2. Exportation of the application using [PyInstaller](https://www.pyinstaller.org/) is not working because of the GUI created by Tkinter. There are no known solutions on the Internet for a black screen showing instead of the button and progress bar. After some research and debugging, this problem seems to be caused purely by Tkinter, and there is no fix.
    - This is the command I'm currently using to build the executable using PyInstaller (note that *username* is used to censor my actual username):  

    pyinstaller moody_playlist.py -w --onefile \\  
    \-\-collect-all librosa \\  
    \-\-paths=/Users/username/Desktop/Music_Project/pyAudioAnalysis/ \\  
    \-\-paths=/opt/anaconda3/envs/music/lib/python3.8/site-packages/ \\  
    \-\-collect-all tkinter \\  
    \-\-add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' \\  
    \-\-add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'