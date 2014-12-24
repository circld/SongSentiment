Author: Paul Garaud

# Description
This module allows the downloading and visualization of Billboard Hot-100 songs. Sentiment scores are produced using [AlchemyAPI](http://www.alchemyapi.com/api/calling-the-api/).

# Installation
This project imports [billboard.py](https://github.com/guoguo12/billboard-charts) and [AlchemyAPI](https://github.com/AlchemyAPI/alchemyapi_python) placed in your site-packages folder in folders called billboard and alchemyapi, respectively. You will also need to add a blank __init__.py file to the billboard folder for Python to recognize it as a module.

Please note that for the pickled data to load properly, you should probably use Python 2.7.5.

# Possible future extensions
Ways I would like to extend this module include adding __cmp__, __eq__, and __hash__ to the ChartSentiment class in order to ensure uniqueness in the unpickle_charts (ordering of pickled objects is currently enforced only by naming convention, and overlapping date ranges will lead to erroneous charts.

I also would like to implement an instance of the SongData class as a global variable that will be preserved via pickle_charts. This wastes up to 100 songs per run of the program in terms of API calls, and makes it impossible to access individual song lyrics and sentiment scores across sessions.

The tests associated with the projects do not cover some of the functionality added late into the project and needs to be updated.

Analysis was not ultimately possible, as priority was given to ensuring that the data retrieval, archiving, and visualization portions of the project were completed and functional. A major bottleneck to development came from the AlchemyAPI transaction limit of 1,000 per day, making debugging very costly and introduced a trade-off between development and downloading data.
