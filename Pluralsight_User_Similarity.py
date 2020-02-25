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

# +
import pandas as pd
import seaborn as sns
import numpy as np

from scipy.sparse import csr_matrix

from sklearn.metrics.pairwise import cosine_similarity

from gensim.models import Word2Vec, KeyedVectors

import nltk

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
#Obtaining total time viewed and total counts with respect to user and course id

aggregated_courseViews_df = courseViews_df.groupby(['user_handle', 'course_id']).agg({'view_time_seconds':['sum'], 'view_date':['count']})

aggregated_courseViews_df.columns= ['total_view_time_seconds', 'total_view_count']

aggregated_courseViews_df = aggregated_courseViews_df.reset_index()

aggregated_courseViews_df

# +
#Normalizing the view counts using min max scalar

print(aggregated_courseViews_df.total_view_count.mean())
print(aggregated_courseViews_df.total_view_count.max())
print(aggregated_courseViews_df.total_view_count.min())

aggregated_courseViews_df['total_view_normalized'] = aggregated_courseViews_df['total_view_count'] - aggregated_courseViews_df['total_view_count'].min()

aggregated_courseViews_df['total_view_normalized'] = aggregated_courseViews_df['total_view_count']/aggregated_courseViews_df.total_view_count.max()

aggregated_courseViews_df

# +
#Normalising view-time using min-max scalar

print(aggregated_courseViews_df.total_view_time_seconds.mean())
print(aggregated_courseViews_df.total_view_time_seconds.max())
print(aggregated_courseViews_df.total_view_time_seconds.min())

aggregated_courseViews_df['seconds_normalized'] = aggregated_courseViews_df['total_view_time_seconds'] - aggregated_courseViews_df['total_view_time_seconds'].min()

aggregated_courseViews_df['seconds_normalized'] = aggregated_courseViews_df['total_view_time_seconds']/aggregated_courseViews_df.total_view_time_seconds.max()

aggregated_courseViews_df['seconds_normalized'] = aggregated_courseViews_df['seconds_normalized']*10
aggregated_courseViews_df['total_view_normalized'] = aggregated_courseViews_df['total_view_normalized']*10




# +
#No.of Users and Courses
users = aggregated_courseViews_df['user_handle'].unique()
courses = aggregated_courseViews_df['course_id'].unique()

print(users.shape)
print(courses.shape)


courses_final = aggregated_courseViews_df

#courses2 = courseViews_df.groupby(['user_handle']).head(5000)
#courses2


courses_final['users_index'] = courses_final['user_handle'].apply(lambda x : np.argwhere(users == x)[0][0])
courses_final['courses_index'] = courses_final['course_id'].apply(lambda x : np.argwhere(courses == x)[0][0])

courses_final
#courses2

#Drop all the unnecessary columns
courses_final=courses_final.drop(['user_handle', 'course_id', 'total_view_time_seconds', 'total_view_count'], axis = 1)



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

# +
time_weight = 0.6
view_weight = 0.4

courses_final['weighted_value'] = (time_weight * courses_final['seconds_normalized']) + (view_weight * courses_final['total_view_normalized'])

courses_final

# +
occurences = csr_matrix((courses_final.weighted_value, (courses_final.users_index, courses_final.courses_index)))

print(occurences)

# +
user_similarity = cosine_similarity(occurences)
print(user_similarity)

similarities_sparse = cosine_similarity(occurences,dense_output=False)
print('pairwise sparse output:\n {}\n'.format(similarities_sparse))
# -

#Final similarity arrays and similarity scores between every other user
result1 = np.flip(np.sort(user_similarity, axis=1), axis=1)
result1_indices = np.flip(np.argsort(user_similarity, axis=1), axis=1)



# +
#Useful observations

#every course viewed by many customers
# users_grouped = courseViews_df.groupby('course_id')['user_handle'].unique().apply(list)
# users_grouped

# courses_grouped = courseViews_df.groupby('user_handle')['course_id'].unique().apply(list)
# courses_grouped

# +
#Converted the results matrix into pickle dump, to use it in an API
# import pickle

# pickle.dump(result1_indices, open("result_indices.pkl", "wb"))

# +
# print(courseViews_df.size)
# print(coursetags_df.size)

# dfx = pd.merge(courseViews_df, coursetags_df, how = 'inner', on='course_id')

# dfx.size

# +
coursetags_df['course_tags'] = coursetags_df['course_tags'].astype('str') 
tags = coursetags_df['course_tags'].values

#print(tags)

tagsVec = [nltk.word_tokenize(tag) for tag in tags]

# +
model = Word2Vec(tagsVec, min_count = 1, size = 32)

model.most_similar('python')
