import requests


if __name__ == '__main__':

    r = requests.get("http://127.0.0.1:8081/bbbb")
    print("Status Code:" + str(r.status_code))
    print(r)
