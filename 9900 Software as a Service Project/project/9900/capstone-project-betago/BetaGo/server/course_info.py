import json
# index in db and then giving response
def course_action(action,intents,params):
    # action Course
    if action == "Course_Info":
        # load course json db
        path = 'data/db.json'
        with open(path) as f:
            data = json.load(f)

        courseID = params["course"].upper()

        # parse message according to different user intents

        if intents == "courseInfo":
            meassage = data[courseID]

        elif intents == "Overview":
            message = "The Overview of "+ courseID +" is: \n"+ data[courseID]["overview"]

        elif intents =="lecturer":
            message = ""

            try:
                if data[courseID]["term one"]:
                    message += "Term one: \nLecturer is: " + data[courseID]["term one"]["lecturer"] +"<br>"
            except:
                pass
            try:
                if data[courseID]["term two"]:
                    message += "Term two: \nLecturer is: " + data[courseID]["term two"]["lecturer"] +"<br>"
            except:
                pass
            try:
                if data[courseID]["term three"]:
                    message += "Term three: \nLecturer is: " + data[courseID]["term two"]["lecturer"] + "<br>"
            except:
                pass
        elif intents == 'Timetable':
            message = "You can check course " + courseID + " timetable in course outline link: "\
            + "<a href = \""+ data[courseID]["course outline link"]+ "\" target = \"_blank\"> Link </a>"

        elif intents == "Faculty":
            faculty = data[courseID]["faculty"]
            school = data[courseID]["school"]
            message = "Faculty: " + faculty + ", School: " + school

        elif intents == 'Terms':
            message = "This course is offering at terms: "+ data[courseID]["offering terms"]

        elif intents == 'Credits':
            message = data[courseID]["unit of credit"]

        elif intents == 'Fees':
            domestic_fees = data[courseID]["domestic fees"]
            commonwealth_fees = data[courseID]["commonwealth fees"]
            international_fees = data[courseID]["international fees"]
            message = "domestic fees is :" + domestic_fees + "\n" +\
                     "commonwealth_fees is :" + commonwealth_fees + "\n" +\
                      "international fees is :" +international_fees

        elif intents == 'Handbook':
            message = "The handbook link is: <br>" + \
                      "<a href = \""+ data[courseID]["handbook link"]+ "\" target = \"_blank\"> Link </a>"
        elif intents == 'Outline_Link':
            message = "The outline link is: <br>" \
                      "<a href = \"" + data[courseID]["course outline link"] + "\" target = \"_blank\"> Link </a>"
        elif intents =='check_adk':
            try:
                if data[courseID]["ADK"] == "true":
                    message = "The course " + courseID + " is an ADK course."
                else:
                    message = "The course " + courseID + " is not an ADK course."
            except:
                message = "Sorry, the information about the course may not be release in our database."

        # if there is not this kind of intents
        else:
            message = "There is not this model"

    # action Stream
    if action =="Stream_Info":
        path = 'data/stream.json'
        # load stream json db
        with open(path) as f:
            data = json.load(f)
        streamName = params["stream"]
        for i in data:
            if data[i]["name"] == streamName:
                data = data[i]
                break
        if intents == "stream_detail":
            message = "The overview of " + data["name"] + " is: <br>" + data["overview"] +"<br><br>" +\
                      "The minimum units of credit is: " + data["minimum units of credit"] +"<br><br>"+\
                      data["core courses description"] +"<br>"+ "core courses list: "
            course_list = " ".join(data["core courses list"])
            message += course_list

        else:
            message = "There is not this model"


    return message


