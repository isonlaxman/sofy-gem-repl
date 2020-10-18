import requests
import json
import os

CONFIG = {}

with open('./config.json') as f:
    CONFIG = json.load(f)

global_headers = {
    'admin': CONFIG["admin"],
}

base_url = "http://58341c1b5233.ngrok.io"

def init_database():
    url = base_url + "/sofy-firebase-backend/us-central1/api/sigma/initDatabase"

    payload = {}

    response = requests.request(
        "POST", url, headers=global_headers, data=payload)
    return json.loads(response.text)["data"]["userId"]

def delete_database():
    url = base_url + "/sofy-firebase-backend/us-central1/api/sigma/deleteDatabase"

    payload = {}

    requests.request(
        "POST", url, headers=global_headers, data=payload)

    return "Data deleted"


def get_weights(userId):
    url = base_url + "/sofy-firebase-backend/us-central1/api/sigma/user/getWeights?userId=" + userId

    payload = {}

    response = requests.request(
        "GET", url, headers=global_headers, data=payload)
    return json.loads(response.text)["data"]["weights"]


def get_gem(userId):
    url = base_url + "/sofy-firebase-backend/us-central1/api/sigma/user/getGem"

    payload = {"userId": userId, "lastGemTime": None}

    response = requests.request("POST", url, headers=global_headers, json=payload)
    return json.loads(response.text)["data"]["gem"]


def heart(userId, gemId):
    url = base_url + "/sofy-firebase-backend/us-central1/api/sigma/userGem/heart"

    payload = {
        "userId": userId,
        "gemId": gemId
    }

    response = requests.request(
        "POST", url, headers=global_headers, json=payload)

    return json.loads(response.text)

def read(userId, gemId):
    url = base_url + "/sofy-firebase-backend/us-central1/api/sigma/userGem/read"

    payload = {
        "userId": userId,
        "gemId": gemId
    }

    response = requests.request(
        "POST", url, headers=global_headers, json=payload)

    return json.loads(response.text)


gemGroupMap = {
    0: "seen",
    1: "heart",
    2: "new"
}

path_count_map = {}

def get_relevant_info(chosenGem, weights):
    retVal = {}

    gem_name = ""
    path_id = chosenGem["pathId"]
    gem_id = chosenGem["id"]

    if path_id in path_count_map:
        if gem_id not in path_count_map[path_id]:
            path_count_map[path_id][gem_id] = path_id + " " + str(path_count_map[path_id]["count"] + 1)
            path_count_map[path_id]["count"] += 1
    else:
        path_count_map[path_id] = {
            "count": 1, 
            gem_id: path_id + " " + str(1)
        }

    gem_name = path_count_map[path_id][gem_id]

    for gi, g in enumerate(weights):
        for _, p in enumerate(g["items"]):
            if p["id"] == chosenGem["pathId"]:
                retVal["group"] = {
                    "weight": g["weight"], "name": "connections" if gi == 0 else "non-connections"}
                retVal["path"] = {"weight": p["weight"], "id": p["id"]}

                for ggi, gg in enumerate(p["gemGroups"]):
                    for _, gem in enumerate(gg["gems"]):
                        if gem["id"] == chosenGem["id"]:
                            retVal["gemGroup"] = {"name": gemGroupMap[ggi]}
                            retVal["gem"] = {
                                "name": gem_name
                            }

                break

    return retVal


def pre_loop():
    # os.system("firebase firestore:delete --all-collections -y")
    id = init_database()
    return id


userId = pre_loop()
print(userId)


print("\n\nWelcome to Sofy's weight testing script")

# get gem -> show old weight -> heart/skip -> show new weight
while True:
    gem = get_gem(userId)

    curr_weights = get_weights(userId)
    print("\nWeight", get_relevant_info(gem, curr_weights))

    i = input("Press h to heart and s to skip. Press q to quit once done\n")

    while True:
        if (i == "h"):
            heart(userId, gem["id"])
            break
        elif (i == "s"):
            read(userId, gem["id"])
            break
        elif (i == "q"):
            delete_database()
            quit()
        else:
            print("Invalid input, please type h, s, or q")
            continue

    curr_weights = get_weights(userId)
    print("\nUpdated weight", get_relevant_info(gem, curr_weights))
