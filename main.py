import pandas as pd

r_cols= ["user_id", "movie_id", "rating"]
ratings= pd.read_csv("user.csv", names=r_cols, usecols=range(3), encoding= 'unicode_escape')

m_cols= ["movie_id", "title"]
movies= pd.read_csv("movies.csv", names=m_cols, usecols=range(2), encoding= 'unicode_escape')

ratings= pd.merge(movies, ratings)

#print(ratings.head())


userRatings= ratings.pivot_table(index=['user_id'], columns=['title'], values='rating')
#print(userRatings.head())


# corrMatrix= userRatings.corr()
# This give correlation score between every pair of movies
# this matrix gives similarity score of any 2 movies

# movie must be rated by more that 100 peoples
corrMatrix= userRatings.corr(method='pearson', min_periods=100)
#print(corrMatrix.head())


user_number= int(input('Please enter user id of user to whom you would like to recommend movies : '))
myRating= userRatings.loc[user_number].dropna()
print('List of movies & ratings given by user :')
print(myRating)
print()

simCandidates= pd.Series([], dtype=pd.StringDtype())
for i in range(0, len(myRating.index)):
    print('Adding sims for '+ myRating.index[i]+".....")
    # Retrieve similar movies to this one I rated
    sims= corrMatrix[myRating.index[i]].dropna()
    # now scale its similarity by how well I rated this movie
    sims= sims.map(lambda x: x * myRating[i])
    # Add score to the list of similarity candidates
    simCandidates= simCandidates.append(sims)

#print(simCandidates.head())
print()

# Glance at our result so far
simCandidates= simCandidates.groupby(simCandidates.index).sum()
simCandidates.sort_values(inplace=True, ascending=False)
#print(simCandidates.head(20))


for i in simCandidates.index:
    for j in myRating.index:
        if i==j:
            simCandidates.drop(i, inplace= True)


print("We are recommending bellow 20 movies for this user!")
print(simCandidates.head(20))