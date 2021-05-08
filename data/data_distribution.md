# Data Overview

Last Updated: May 7, 2021

This document contains some general information about the data used for training the models.
A total of 200 MP3 files were labeled with a primary mood and a secondary mood for the supervised 
learning algorithms. Here are some statistics about the songs and their features:

### Primary Mood Distribution
This is the distribution of primary moods:  
![Primary Mood Distribution](primary_dist.jpg)

### Secondary Mood Distribution
This is the distribution of secondary moods:  
![Secondary Mood Distribution](secondary_dist.jpg)

### Top Ten Artists
Here are the top ten most frequent artists (with number of songs included):  
<pre>
Takanashi Yasuharu          <b>18</b>  
One Direction               <b>13</b>  
Super Junior                <b>12</b>  
Two Steps From Hell         <b>10</b>  
Sereno                      <b>07</b>  
Taylor Swift                <b>05</b>  
Yamagami Takeshi            <b>04</b>  
Yiruma                      <b>04</b>  
VK                          <b>04</b>  
Toshiro Masuda              <b>03</b>  
</pre>

### Correlation Matrix of 5 Basic Features
One set of features are referred to as the [basic features](features.csv). The basic features only include
the tempo, chroma number, zero crossing rate, energy entropy, and spectral centroid of each MP3 file.
This is the correlation matrix of the five basic features for all 200 MP3 files:  
![Correlation Matrix Basic](correlation_matrix.jpg)

### Correlation Matrix of 28 Engineered Features
One set of features are referred to as the [engineered features](engineered_features.csv). The data distributions
of all features extracted using the package pyAudioAnalysis were analyzed to choose the features with greatest 
variation among primary moods. This is the correlation matrix of the 28 chosen/engineered features for all 200 MP3 files:  
![Correlation Matrix Engineered](eng_correlation_matrix.jpg)

### Data Distribution Plots of Engineered Features
Here are the data distributions as separated by primary mood for each of the 28 engineered features:

#### Tempo
![tempo](feature_dist/primary_dist_tempo.jpg)
#### Chroma Number
![chroma_number](feature_dist/primary_dist_chroma_number.jpg)
#### Zero Crossing Rate Mean
![zcr_mean](feature_dist/primary_dist_zcr_mean.jpg)
#### Zero Crossing Rate Standard Deviation
![zcr_std](feature_dist/primary_dist_zcr_std.jpg)
#### Energy Mean
![energy_mean](feature_dist/primary_dist_energy_mean.jpg)
#### Energy Entropy Mean
![energy_entropy_mean](feature_dist/primary_dist_energy_entropy_mean.jpg)
#### Spectral Centroid Mean
![spectral_centroid_mean](feature_dist/primary_dist_spectral_centroid_mean.jpg)
#### Spectral Spread Mean
![spectral_spread_mean](feature_dist/primary_dist_spectral_spread_mean.jpg)
#### Spectral Entropy Mean
![spectral_entropy_mean](feature_dist/primary_dist_spectral_entropy_mean.jpg)
#### Mel-Frequency Cepstrum Coefficient 2 Mean
![mfcc_2](feature_dist/primary_dist_mfcc_2_mean.jpg)
#### Mel-Frequency Cepstrum Coefficient 5 Mean
![mfcc_5](feature_dist/primary_dist_mfcc_5_mean.jpg)
#### Mel-Frequency Cepstrum Coefficient 6 Mean
![mfcc_6](feature_dist/primary_dist_mfcc_6_mean.jpg)
#### Spectral Centroid Standard Deviation
![spectral_centroid_std](feature_dist/primary_dist_spectral_centroid_std.jpg)
#### Spectral Entropy Standard Deviation
![spectral_entropy_std](feature_dist/primary_dist_spectral_entropy_std.jpg)
#### Spectral Spread Standard Deviation
![spectral_spread_std](feature_dist/primary_dist_spectral_spread_std.jpg)
#### Chroma 7 Standard Deviation
![chroma_7_std](feature_dist/primary_dist_chroma_7_std.jpg)
#### Delta Chroma 2 Standard Deviation
![delta_chroma_2_std](feature_dist/primary_dist_delta_chroma_2_std.jpg)
#### Delta Chroma 3 Standard Deviation
![delta_chroma_3_std](feature_dist/primary_dist_delta_chroma_3_std.jpg)
#### Delta Chroma 9 Standard Deviation
![delta_chroma_9_std](feature_dist/primary_dist_delta_chroma_9_std.jpg)
#### Delta Chroma Standard Deviation's Standard Deviation
![delta_chroma_std_std](feature_dist/primary_dist_delta_chroma_std_std.jpg)
#### Delta Energy Standard Deviation
![delta_energy_std](feature_dist/primary_dist_delta_energy_std.jpg)
#### Delta Mel-Frequency Cepstrum Coefficient 1 Standard Deviation
![delta_mfcc_1_std](feature_dist/primary_dist_delta_mfcc_1_std.jpg)
#### Delta Mel-Frequency Cepstrum Coefficient 3 Standard Deviation
![delta_mfcc_3_std](feature_dist/primary_dist_delta_mfcc_3_std.jpg)
#### Delta Mel-Frequency Cepstrum Coefficient 13 Standard Deviation
![delta_mfcc_13_std](feature_dist/primary_dist_delta_mfcc_13_std.jpg)
#### Delta Spectral Centroid Standard Deviation
![delta_spectral_centroid_std](feature_dist/primary_dist_delta_spectral_centroid_std.jpg)
#### Delta Spectral Entropy Standard Deviation
![delta_spectral_entropy_std](feature_dist/primary_dist_delta_spectral_entropy_std.jpg)
#### Delta Spectral Flux Standard Deviation
![delta_spectral_flux_std](feature_dist/primary_dist_delta_spectral_flux_std.jpg)
#### Delta Spectral Spread Standard Deviation
![delta_spectral_spread_std](feature_dist/primary_dist_delta_spectral_spread_std.jpg)