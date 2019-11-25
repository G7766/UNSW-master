import json
# index in db and then giving response
def knowledge_action(action,intents,params,question):
    path = 'data/knowledge/knowledge.json'
    # load knowledge json db
    with open(path) as f:
        data = json.load(f)

    try:
        # print(json.dumps(data, indent=4))
        # print(params)
        key = params["Knowledge1"]
        if intents == "Knowledge_description":
            message = key + ": " + data[key]["description"]
        elif intents == "Knowledge_properties":
            message = "The properties of "+key+" is: <br>" + data[key]["properties"]
        elif intents == "Knowledge_how_to_code":
            message = "The way to code the "+key+" is: <br>" + data[key]["how to code"]
        elif intents == "Knowledge_advantages":
            message = "The advantages of "+key+" is: <br>" + data[key]["advantages"]
        elif intents == "Knowledge_disadvantages":
            message = "The disadvantages of "+key+" is: <br>" + data[key]["disadvantages"]
        elif intents == "Knowledge_examples":
            message = "The examples of " + key + " is: <br>" + data[key]["example"]
    except:
        # if error response google search with question
        message = "Sorry, we don't have this knowledge in our database, or you can check the knowledge in google link: <br>" +\
          "<a href = \"http://google.com/search?q=" + question +"\" target = \"_blank\"> Link </a>"

    return message