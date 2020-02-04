import numpy as np
import pandas as pd
import math
#read from the databases
Ratings=pd.read_csv("ratings.csv")
Movies=pd.read_csv("movies.csv")
Tags=pd.read_csv("tags.csv")

#Tf stands for term frequency - how often something shows up in database
#IDF stands for inverse document frequency the more a term appears in a database the lower the value is and vice versa
#multiply the two to get a weight of a certain tag

#get tf value and idf value to get TF-IDF value
#tf value
Tf=Tags.groupby(['movieId','tag'], as_index = False, sort = False).count().rename(columns = {'userId': 'tag_count_TF'})[['movieId','tag','tag_count_TF']]

Tag_distinct = Tags[['tag','movieId']].drop_duplicates()#rid of repeats
#df value
DF =Tag_distinct.groupby(['tag'], as_index = False, sort = False).count().rename(columns = {'movieId': 'tag_count_DF'})[['tag','tag_count_DF']]

a=math.log10(len(np.unique(Tags['movieId'])))
#getting values for idf
DF['IDF']=a-np.log10(DF['tag_count_DF'])
#getting values for tf
TF = pd.merge(TF,DF,on = 'tag', how = 'left', sort = False)
#multiplying to get tf-idf
TF['TF-IDF']=TF['tag_count_TF']*TF['IDF']

#unit length vector
#divide tf-idf by vector length of a movie
Vect_len=TF[['movieId','TF-IDF']]
Vect_len['TF-IDF-Sq']=Vect_len['TF-IDF']**2
Vect_len =Vect_len.groupby(['movieId'], as_index = False, sort = False).sum().rename(columns = {'TF-IDF-Sq': 'TF-IDF-Sq-sum'})[['movieId','TF-IDF-Sq-sum']]
Vect_len['vect_len'] = np.sqrt(Vect_len[['TF-IDF-Sq-sum']].sum(axis=1))
TF = pd.merge(TF,Vect_len,on = 'movieId', how = 'left', sort = False)
TF['TAG_WT']=TF['TF-IDF']/TF['vect_len']

#unweighted user profile
#user profile sum of item-tag vectors of items user has rated positively
#in this case a something is positive is greater than 3.5 stars
#get ratings of greater than 3.5 "good movies"
Ratings_filter=Ratings[Ratings['rating']>=3.5]
#get unique users
distinct_users=np.unique(Ratings['userId'])
user_tag_pref=pd.DataFrame()
i=1
#constructing user profiles for distinc users
for user in distinct_users[1:2]:
 
   if i%30==0:#out of the length of uesrs
       print('user: ', i , 'out of: ', len(distinct_users))
 
   user_data= Ratings_filter[Ratings_filter['userId']==user]
   user_data = pd.merge(TF,user_data,on = 'movieId', how = 'inner', sort = False)
   user_data1 = user_data.groupby(['tag'], as_index = False, sort = False).sum().rename(columns = {'TAG_WT': 'tag_pref'})[['tag','tag_pref']]
   user_data1['user']=user
   user_tag_pref = user_tag_pref.append(user_data1, ignore_index=True)
   i=i+1


#Now for all user profiles  compare them to the item profiles and calculate similairty between the twolinefunc



#users

distinct_users=np.unique(Ratings_filter['userId'])
tag_merge_all=pd.DataFrame()
i=1
for user in distinct_users[1:2]:
 
 user_tag_pref_all= user_tag_pref[user_tag_pref['user']==user]
 distinct_movies = np.unique(TF['movieId'])
 j=1
 for movie in distinct_movies:
 
     if j%300==0:
 
         print ('movie: ', j , 'out of: ', len(distinct_movies) , 'with user: ', i , 'out of: ', len(distinct_users))
 
     TF_Movie= TF[TF['movieId']==movie]
     tag_merge = pd.merge(TF_Movie,user_tag_pref_all,on = 'tag', how = 'left', sort = False)
     tag_merge['tag_pref']=tag_merge['tag_pref'].fillna(0)
     tag_merge['tag_value']=tag_merge['TAG_WT']*tag_merge['tag_pref']
 
     TAG_WT_val=np.sqrt(np.sum(np.square(tag_merge['TAG_WT']), axis=0))
     tag_pref_val=np.sqrt(np.sum(np.square(user_tag_pref_all['tag_pref']), axis=0))
 
     tag_merge_final = tag_merge.groupby(['user','movieId'])[['tag_value']].sum().rename(columns = {'tag_value': 'Rating'}).reset_index()
 
     tag_merge_final['Rating']=tag_merge_final['Rating']/(TAG_WT_val*tag_pref_val)
 
     tag_merge_all = tag_merge_all.append(tag_merge_final, ignore_index=True)
     j=j+1
     i=i+1
     tag_merge_all=tag_merge_all.sort_index(by=['user','Rating']).reset_index()