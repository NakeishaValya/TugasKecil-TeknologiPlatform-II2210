import requests
import pyotp
import base64

userid = "vaelya"
shared_secret = "ii2210_vaelya"

server_url = "http://70.153.208.25:17787/motd"

messages = [
    "Semangat!", 
    "Jangan lupa bobo",
]

# generate TOTP
s = base64.b32encode(shared_secret.encode("utf-8")).decode("utf-8")
totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
current_otp = totp.now()

# buat header Authorization
credentials = f"{userid}:{current_otp}"
auth_header = "Basic " + base64.b64encode(credentials.encode("ascii")).decode("ascii")

# kirim semua pesan satu per satu
for msg in messages:
    motd = {"motd": msg}
    response = requests.post(
        url=server_url,
        headers={"Authorization": auth_header},
        json=motd
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.content.decode('utf-8')}")
