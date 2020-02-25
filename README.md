# Collaborative-Filtering-Recommendation-System

This project provides Python implementation of collaborative filtering to find similarity between users, based on implicit feedback. The data consists of implicit feed back such as user interests, assessment scores and so on, which needs to be translated into user course rating matrix. 

**Architecture Overview**:
This implementation has 3 components:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)Pre-processing and exploring the data  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)Identifying user-user similarity  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)API development to extract the first 10 similar users  


**Preprocessing Steps and Feature Engineering**  
Extracted only those user records who has watched a particular course from a time greater than 10 minutes. Also, grouped the data based on number of times a user had watched a particular course. Features I have planned to use are:  
1)Course tags of course ids: Observed one to many relationship between course id and course tags. Hence, vectorizing each coursetag and obtaining a mean of all the course tags can possible capture the relation between course-id and all corresponding paths.  
2)View time of a particular course :This shows how much a user is interested in data.  
3)View count: This count tracks how many times a user had viewed the course.  

**User-User Similarity**
To find the user-user similarity, as per collaborative filtering approach, we first need to construct a user-course rating matrix. To obtain this matrix, we have re-indexed the user-handle and course-id indices and combined the features described above with random weights. From there, I have used **cosine similarity** to calculate the similarity between users.

**API which takes user-handle and returns 10 similar users**
Used Flask to expose the first 10 similar users of a particular user_handle. Similarity matrix obtained from the previous step is wrapped inside a Flask framework which takes user-handle as input and outputs the forst 10 similar users.

**Tools Used**
Python 3.7, Pandas, Scipy, Gensim.Word2Vec, sklearn

**Tools Used**
Python 3.7, Pandas






