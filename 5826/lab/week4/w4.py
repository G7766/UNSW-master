# Your code goes here.
# hcat
#head(X,5)
FX = hcat(data, actors, directors, genres,'revenue_(millions)')
head(FX,5)
FX = clean(FX)
FY = FX['revenue_(millions)']
FX = exclude(X, ['revenue_(millions)','metascore'])
# remove columns
# scale
Fmodel = LinearModel(scale = True)
# model
Fmodel.fit(FX, FY)
Fpredictions = Fmodel.predict(FX)
    #print(Fpredictions[0:10])
# plot
Fmodel.plot(Fpredictions, FY)
# coefficients
Fmodel.coefficients(plot = True, top = 50)

# analyse
#highest
Fmodel.analyse(plot = True, column = 'director_(J.J.Abrams)')
#loest
Fmodel.analyse(plot = True, column = 'director_(ChristopherNolan)')
# Then, recommendations to studios
#I recommend ChristopherNolan to be a directors, because it is obviously to see that, 
#if ChristopherNolan didn't direct movies, the REDUCE the overall mean score 
# by 237.04 millions!!! so he is the person who can make the movie make highest benefit.