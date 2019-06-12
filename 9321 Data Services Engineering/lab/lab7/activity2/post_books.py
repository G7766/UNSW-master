import requests


if __name__ == '__main__':
    book = {
        "Date of Publication": 2018,
        "Publisher": "UNSW",
        "Author": "Nobody",
        "Title": "Nothing",
        "Flickr URL": "http://somewhere",
        "Identifier": 3,
        "Place of Publication": "Sydney"
    }

    r = requests.post("http://127.0.0.1:8081/books", json=book)
    print("Status Code:" + str(r.status_code))
    resp = r.json()
    print(resp['message'])
