import json
import re

# The function is for creating dialogflow entities
# load db path and knowledge path
# creating create_course_entity with json format and upload it to dialogflow
# creating create_knowledge_entity with json format and upload it to dialogflow

def create_course_entity(db_path,output_path):
    with open(db_path) as f:
        data = json.load(f)

    course = {
        "id": "543402ce-5be5-4db3-bc4f-daf2ff17fe86",
        "name": "course",
        "isOverridable": True,
        "entries":[],
        "isEnum": False,
        "automatedExpansion": True,
        "allowFuzzyExtraction": True,
        "isRegexp": False
    }
    for each_course in data:
        change_name = re.sub('[(){}<>]', '', data[each_course]["name"])
        course["entries"].append(
            {
                "value": each_course.lower(),
                "synonyms": [
                    each_course.upper(),
                    change_name,
                    change_name.lower(),
                    change_name.upper(),
                    each_course[-4:],

                ]
            }
        )

    with open(output_path+"course.json","w") as file:
        json.dump(course, file, indent=4, sort_keys=False)
    # with open(output_path+"weather.json","w") as file:
    #     json.dump(weather, file, indent=4, sort_keys=False)


    return


def create_knowledge_entity(knowledge_path,output_path):
    with open(knowledge_path) as f:
        data = json.load(f)

    Knowledge = {
        "id": "543402ce-5be5-4db3-bc4f-daf2ff17fe86",
        "name": "Knowledge1",
        "isOverridable": True,
        "entries":[],
        "isEnum": False,
        "automatedExpansion": True,
        "allowFuzzyExtraction": True,
        "isRegexp": False
    }
    for each_knowledge in data:
        Knowledge["entries"].append(
            {
                "value": each_knowledge.lower(),
                "synonyms": [
                    each_knowledge.upper(),
                    each_knowledge,
                    each_knowledge.lower(),
                    each_knowledge.title(),

                ]
            }
        )

    with open(output_path+"knowledge.json","w") as file:
        json.dump(Knowledge, file, indent=4, sort_keys=False)
    return




if __name__ =="__main__":
    db_path = "data/db.json"
    output_path = "./entities/"
    create_course_entity(db_path,output_path)

    knowledge_path = "data/knowledge/knowledge.json"
    output_path = "./entities/"
    create_knowledge_entity(knowledge_path,output_path)
