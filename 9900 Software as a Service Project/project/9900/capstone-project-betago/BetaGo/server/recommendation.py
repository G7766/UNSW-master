import json
# index in db and then giving response
def recommendation_action(action,intents,params):
    if action == "Recommendation":
        if intents == "course_Similarity":

            path = 'data/recommendation/course_similarity.json'
            with open(path) as f:
                data = json.load(f)

            # print(json.dumps(data, indent=4))

            courseID = params["course"].upper()
            courseID = courseID.upper()

            message = "The course similar to "+ courseID +" is: <br>" + data[courseID]

        if intents == "course_Category":

            #print(params)
            path = 'data/recommendation/course_category.json'
            with open(path) as f:
                data = json.load(f)

            #print(json.dumps(data, indent=4))

            # category = ['algorithm', 'application', 'data', 'python',
            #             'software', 'network', 'neural', 'system', 'artificial',
            #             'IoT', 'security', 'engage', 'digital', 'distributed',
            #             'blockchain', 'search', 'compression', 'C', 'C++',
            #             'hardware', 'wireless', 'vision']

            #print(params['Category'])
            try:
                key = params['Category']
                course = []
                for i in data:
                    l = data[i]["category"].split()
                    if key in l:
                        course.append(i)
                message = "The course relate to "+ key + " is: <br>" + " ".join(course)
                if course == []:
                    # if not course in list
                    message = "Sorry we don't have this category."


            except:
                message = "Sorry we don't have this category."


    return message
