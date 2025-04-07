import requests
import pyotp
import base64

userid = "vaelya"
shared_secret = "ii2210_vaelya"

server_url = "http://70.153.208.25:17787/motd"

motd = {"motd": "haihai"}

# generate TOTP
s = base64.b32encode(shared_secret.encode("utf-8")).decode("utf-8")
totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
current_otp = totp.now()

# buat header Authorization
credentials = f"{userid}:{current_otp}"
auth_header = "Basic " + base64.b64encode(credentials.encode("ascii")).decode("ascii")

# kirim POST request
response = requests.post(
    url=server_url,
    headers={"Authorization": auth_header},
    json=motd
)

# tampilkan hasil response
print(response.status_code)
print(response.content.decode("utf-8"))
