#!/bin/bash
jupyter nbconvert --to html data_overview.ipynb
jupyter nbconvert --to html models/training_models.ipynb
jupyter nbconvert --to html music/feature_extraction.ipynb