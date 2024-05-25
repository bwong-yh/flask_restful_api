import requests

BASE = "http://127.0.0.1:5000/"

payloads = [
    {"name": "funny cat", "views": 100, "likes": 82},
    {"name": "chubby baby", "views": 345, "likes": 282},
    {"name": "nba highlights", "views": 1223, "likes": 1057}
]

for i in range(len(payloads)):
    vid = i + 1
    res = requests.post(BASE + f"video/{vid}",
                        headers={"Content-Type": "application/json"},
                        json=payloads[i])

    print(res.json(), res.status_code)


res = requests.get(BASE + "video/100")
print(res.json(), res.status_code)


res = requests.post(BASE + "video/2",
                    headers={"Content-Type": "application/json"},
                    json={"name": "chubby baby", "views": 345, "likes": 282})
print(res.json(), res.status_code)

res = requests.delete(BASE + "video/3")
print(res.json(), res.status_code)

res = requests.delete(BASE + "video/3")
print(res.json(), res.status_code)

res = requests.get(BASE + "videos")
print(res.json(), res.status_code)
