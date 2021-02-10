# Setup Guide

Last Updated: February 10, 2021
### Environment Setup
1. Download and install [Anaconda](https://docs.anaconda.com/anaconda/install/)  
    - If you aren't already using Python 3.8 with Anaconda, run the following commands  
        ```python
        conda activate
        conda install -c anaconda python=3.8
        ```
2. Create and switch to an environment named music
    ```python
    conda create --name music python=3.8
    conda activate music
    ```
3. Install the two packages needed: pyAudioAnalysis and librosa
    - [librosa](https://librosa.org/) installation
    ```python
        conda install -c conda-forge librosa
    ```
    - [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis/) installation
        ```python
        git clone https://github.com/tyiannak/pyAudioAnalysis.git
        cd pyAudioAnalysis
        pip install -r requirements.txt
        pip install -e .
        ```