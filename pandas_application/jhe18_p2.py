import pandas as pd
user_artist = pd.read_table('user_artists.dat')
artists = pd.read_table('artists.dat', encoding="utf-8", sep="\t", index_col='id')
user_friend = pd.read_table('user_friends.dat', encoding="utf-8", sep="\t")
# merge the table user_artist and the table artists
user_artist_info = pd.merge(user_artist, artists, left_on='artistID', right_on='id')


# Q1: compute the sum of weight column, group by (artist) name and artistID
group_weight = user_artist_info['weight'].groupby([user_artist_info['name'], user_artist_info['artistID']])
byweight = group_weight.sum().sort_values(ascending=False)[:10]
df_byweight = pd.DataFrame(byweight.values, index=byweight.index)
df_byweight.columns = ['num of song plays']
Q1 = df_byweight


# Q2: count the number of userID, group by (artist) name and artistID
group_listener = user_artist_info['userID'].groupby([user_artist_info['name'], user_artist_info['artistID']])
bylistener = group_listener.count().sort_values(ascending=False)[:10]
df_bylistener = pd.DataFrame(bylistener.values, index=bylistener.index)
df_bylistener.columns = ['num of listeners']
Q2 = df_bylistener


# Q3: compute the sum of weight, group by userID
group_topuser = user_artist['weight'].groupby(user_artist['userID'])
topuser = group_topuser.sum().sort_values(ascending=False)[:10]
df_topuser = pd.DataFrame(topuser.values, index=topuser.index)
df_topuser.columns = ['num of song plays']
Q3 = df_topuser


# Q4: What artists have the highest average number of plays per listener?
# count the number of users for each artist
group_userID = user_artist_info['userID'].groupby([user_artist_info['artistID'], user_artist_info['name']])
user_count = pd.DataFrame(group_weight.count())
user_count.columns = ['user_count']
# calculate the sum of weight for each artist
group_weight = user_artist_info['weight'].groupby([user_artist_info['artistID'], user_artist_info['name']])
weight_sum = pd.DataFrame(group_weight.sum())
weight_sum.columns = ['weight_sum']
# merge the data togather and calculate the average weight for each aritst
avg_weight_info = pd.merge(user_count, weight_sum, left_on='artistID', right_on='artistID')
avg_weight_info['avg_weight'] = avg_weight_info['weight_sum'] / avg_weight_info['user_count']
top_avgweight = avg_weight_info.sort_values(by=['avg_weight'], ascending=False)[:10]
# find the artist name
result = pd.merge(top_avgweight, artists, how='left', left_index=True, right_on='id')
Q4 = result[['name', 'weight_sum', 'user_count', 'avg_weight']]


# Q5: What artists with at least 50 listeners have the highest average number of plays per listener?
# filer the avg_weight_info with a condition: user_count >= 50
avgweight_info_q5 = avg_weight_info.loc[avg_weight_info['user_count'] >= 50]
# sort avgweight_info_q5 and find the artistname
top_avgweight_q5 = avgweight_info_q5.sort_values(by=['avg_weight'], ascending=False)[:10]
result_q5 = pd.merge(top_avgweight_q5, artists, how='left', left_index=True, right_on='id')
Q5 = result_q5[['name', 'weight_sum', 'user_count', 'avg_weight']]


# Q6: Do users with five or more friends listen to more songs?
# count the number of friend for each user
count_group = user_friend['friendID'].groupby(user_friend['userID'])
count_friend = pd.DataFrame(count_group.count())
count_friend.columns = ['friend_count']
# select userID with 5 or more and less than 5 friend
userid_frd_5more = count_friend.loc[count_friend['friend_count'] >= 5]
userid_frd_5less = count_friend.loc[count_friend['friend_count'] < 5]
# calculate average number of plays for userID with 5 or more friends
user_5more = pd.merge(userid_frd_5more, user_artist, how='left', left_on='userID', right_on='userID')
total_plays_m = user_5more['weight'].sum()
total_users_m = user_5more['userID'].count()
avg_5more = total_plays_m / total_users_m
# calculate average number of plays for userID with 5 or more friends
user_5less = pd.merge(userid_frd_5less, user_artist, how='left', left_on='userID', right_on='userID')
total_plays_l = user_5less['weight'].sum()
total_users_l = user_5less['userID'].count()
avg_5less = total_plays_l / total_users_l

Q6 = pd.Series({'average song plays for users with 5 or more friend: ': avg_5more,
                    'average song plays for users with less than 5 friend: ': avg_5less})


# Q7: How similar are two artists?
def artist_sim(aid1, aid2):
    # find the user sets for artist aid1 and aid2
    info_aid1 = user_artist.loc[user_artist['artistID'] == aid1]
    info_aid2 = user_artist.loc[user_artist['artistID'] == aid2]
    user_set1 = set(info_aid1['userID'].unique())
    user_set2 = set(info_aid2['userID'].unique())
    # caclute the jaccard index based on the sets
    jaccard_index = len(user_set1 & user_set2) / len(user_set1 | user_set2)
    return 'The Jaccard Index between user sets of aid1(' + str(aid1) +') and aid2('\
     + str(aid2) + ') is:\n' + str(jaccard_index) + '.'


# Q8: Analysis of top tagged artists
tags = pd.read_table('user_taggedartists.dat', encoding="utf-8", sep="\t")
# merge the user_taggedartists with artists
artist_tags = pd.merge(artists, tags, left_on='id', right_on='artistID')
# find the artists with top 10 tag numbers
top10_tags = artist_tags['tagID'].groupby(artist_tags['artistID']).count().sort_values(ascending=False)[:10]
top10tags_df = pd.DataFrame(top10_tags)
top10tags_df.columns = ['tag_count']
# print the artists' info
artists_info = pd.merge(top10tags_df, artists, how='left', left_index=True, right_on='id')
Q8 = artists_info[['name','tag_count']]




print('Q1: Who are the top artists in terms of play counts?')
print(Q1, '\n')

print('Q2: What artists have the most listeners?')
print(Q2, '\n')

print('Q3: Who are the top users in terms of play counts?')
print(Q3, '\n')

print('Q4: What artists have the highest average number of plays per listener?')
print(Q4,'\n')

print('Q5: What artists with at least 50 listeners have the highest average number of plays per listener?')
print(Q5, '\n')

print('Q6: Do users with five or more friends listen to more songs?')
print(Q6, '\n')

print('Q7: How similar are two artists?')
print(artist_sim(51, 52), '\n')

print('Q8: Analysis of top tagged artists')
print(Q8, '\n')
