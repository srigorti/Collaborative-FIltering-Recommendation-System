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

# +
print("Number of Uniques course tags existing:",coursetags_df.course_tags.unique().size)
print("Number of unique courses existing:",coursetags_df.course_id.unique().size)
print("size of coursetags csv:",coursetags_df.size)

#Meaning, MULTIPLE course tags might exist for a single course_id

# +
#Lets go ahead and find multiple tags assosciated with a single course_id
course_paths = coursetags_df.groupby('course_id')['course_tags'].apply(list).reset_index()

course_paths.head()
# -

courseViews_df.head(5)

# +
print("size of course views csv:",courseViews_df.size)


#Total number of visitos who visited certain courses
print("Number of users",courseViews_df.user_handle.unique().size)

#Total number of courses visited by various users
print("Number of courseid",courseViews_df.course_id.unique().size)



#"Course views for a specific user_handle"
#print(courseViews_df[courseViews_df.user_handle == 7487].sort_values('view_date'))


# print(courseViews_df['course_id'].value_counts().size)

# courseViews_df.head(10)

#print("authorhandle",courseViews_df['author_handle'].unique().size)

# +
#Remove all the records which a user watched less than 10 mins
indexNames = courseViews_df[ (courseViews_df['view_time_seconds'] >= 0) & (courseViews_df['view_time_seconds'] <= 600) ].index
courseViews_df.drop(indexNames , inplace=True)

courseViews_df.size

# +
#Top 15 authors
df4 = courseViews_df.groupby(by='author_handle', as_index=False).agg({'user_handle': pd.Series.nunique})
df4 = df4.sort_values(by='user_handle', ascending = False)

ax2 = df4.head(15).set_index('author_handle').plot(kind='bar', figsize=(45,25), fontsize = 50)
ax2.set_xlabel("Author Handle", fontsize=50)
ax2.set_ylabel("No. of user views", fontsize=50)
ax2

# +
#every course viewed by many customers
users_grouped = courseViews_df.groupby('course_id')['user_handle'].unique().apply(list).reset_index()
#users_grouped.reset_index()
users_grouped.rename(columns = {'course_id': 'course_id', 'Total_views':'user_handle'})

users_grouped
# -

userInterests_df.head(5)

print("size of user interests csv:",userInterests_df.size)
print("number of unique user handles:",userInterests_df['user_handle'].unique().size)
print("number of unique interest_tags:",userInterests_df['interest_tag'].unique().size)

# +
#lets find out top 15 course tags according to user interests

ax = userInterests_df['interest_tag'].value_counts().head(15).plot(kind = 'bar', figsize = (45,25), fontsize=50, title = 'Top 15 courses acc to user interests')
ax.set_xlabel("Course Tag", fontsize=50)
ax.set_ylabel("User Interets", fontsize=50)

ax
# -

assesScores_df.head(5)


