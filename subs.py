import requests, json, os

API_KEY = os.environ["API_KEY"]
NTFY_TOPIC = os.environ["NTFY_TOPIC"]
CHANNEL_ID = "UCrAvFsw0ROe15n8qZQxVi8g"  # Trix (@trix_xc)
STATE_FILE = "subs_count.json"

def get_subs():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    data = requests.get(url).json()
    return int(data["items"][0]["statistics"]["subscriberCount"])

def main():
    current = get_subs()
    previous = None
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            previous = json.load(f)["count"]

    if previous is not None and current > previous:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=f"¡Nuevo suscriptor! Ahora tienes: {current}".encode("utf-8")
        )

    with open(STATE_FILE, "w") as f:
        json.dump({"count": current}, f)

    with open("/tmp/current_count.txt", "w") as f:
        f.write(str(current))

if __name__ == "__main__":
    main()
