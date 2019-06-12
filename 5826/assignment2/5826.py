Q1:
pokemon = read('Pokemon.csv')
Y = pokemon['total']
YY = pokemon.total
pokemon_exclude = exclude(pokemon,col=['#','name','total'])
pokemon_exclude


Q2:
#Type_1
a = tally(pokemon_exclude.type_1,minimum=3,multiple =True )
#Type_2
b = tally(pokemon_exclude.type_2,minimum=3,multiple =True)
#Legendary 
c = tally(pokemon_exclude.legendary,minimum=3,multiple =True)
#Generation
d = tally(pokemon_exclude.generation,minimum=3,multiple =True)
#help(tally)

Q3:
plot(x=pokemon_exclude.type_2,y = Y, colour = pokemon_exclude.type_1)

Q4:
#help(ternary)
t_defence =ternary(pokemon_exclude['defense'],'>60',1,0)
t_hp = ternary(pokemon_exclude['hp'],'>=60',-1,1)
t_speed = ternary(pokemon_exclude['speed'],'<=100',0,1)
#tally(t_defence)
#tally(t_hp)
#tally(t_speed)

Q5：
#help(read_clean)
pokemon_clean = clean(pokemon_exclude)
pokemon_clean = exclude(pokemon_clean,col='legendary')
#pokemon_clean
#help(hcat)
combined_data = hcat(pokemon_clean,a,b,c,d,t_defence,t_hp,t_speed)
combined_data

Q6：
#help(Inference)
model = Inference()
model.fit(combined_data,Y)
model.coefficients()

Q7:
#help(plot)
#help(model.predict)
plot(x = model.predict(combined_data),y = Y, style='regplot',power=1)
#help(model.score)
#model.score(model.predict(combined_data), Y)
# We can score the model using SCORE.The larger absolute values of 0.3 are better.
#so the model isn't that good.


Q8：
#help(ternary)
#help(keep)
m = ['hp','defense','speed','attack','generation','sp._def','sp._atk','total','generation_(4)','type_2_(Dragon)',
    'generation_(6)','generation_(1)']
keep_good_data = combined_data[m].copy()
model_keep_good = Inference()
model_keep_good.fit(keep_good_data,Y)
model_keep_good.coefficients()
# This model is better than than Q7, the pavalue is higher than the model in Q7, which gives a more precisely value
# to represent the situation
Q9：
#The cofficients show that the bigger the value, the more influence to the PVALUES.
# the columns hp\defense\speed\attack\sp_defense\sp_attack are good, cause they got cofficients