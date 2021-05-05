#!/bin/bash
jupyter nbconvert --to html data_overview.ipynb
jupyter nbconvert --to html models/training_models.ipynb
jupyter nbconvert --to html models/deprecated/large_models.ipynb
jupyter nbconvert --to html models/deprecated/neural_network_colab.ipynb
jupyter nbconvert --to html music/feature_extraction.ipynb
jupyter nbconvert --to html music/deprecated/raw_feature_extraction.ipynb
jupyter nbconvert --to html application/moody_playlist.ipynb