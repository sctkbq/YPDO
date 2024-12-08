import requests

timeout = 30

links = []

try:
    for url, data in [
        (
            "https://api.mumuglobal.com/api/v1/download/nemux",
            [
                ("architecture", "x86_64"),
                ("machine", "{}"),
                ("usage", "1"),
            ],
        ),
        (
            "https://mumu.nie.netease.com/api/v1/download/nemux",
            [
                ("architecture", "x86_64"),
                ("machine", "{}"),
                ("usage", "0"),
            ],
        ),
    ]:
        r = requests.post(
            url, timeout=timeout,
            data=data
        )

        j = r.json()

        link = j["data"]["mumu"]["link"]

        link = link.replace("http://", "https://", 1)

        links.append(link)

    with open("mumu.txt", "w") as f:
        for link in links:
            print(link, file=f)

except Exception:
    pass
