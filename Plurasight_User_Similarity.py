# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd

# +
#Reading all the csv files into pandas data frame

userInterests_df = pd.read_csv(r'/Users/vamsichebolu/Desktop/Pluralsight_Take_Home/data/user_interests.csv')
courseViews_df = pd.read_csv(r'/Users/vamsichebolu/Desktop/Pluralsight_Take_Home/data/user_course_views.csv')
assesScores_df = pd.read_csv(r'/Users/vamsichebolu/Desktop/Pluralsight_Take_Home/data/user_assessment_scores.csv')
coursetags_df= pd.read_csv(r'/Users/vamsichebolu/Desktop/Pluralsight_Take_Home/data/course_tags.csv')


# -

coursetags_df.head(5)

courseViews_df.head(5)

userInterests_df.head(5)

assesScores_df.head(5)


