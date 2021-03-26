import time

import requests

from docker_decorators import with_container


@with_container(
    "nginx",
    name="nginx-decorated",
    remove_container=False,
    options={"detach": True, "ports": {80: 80}},
)
def important_function():
    print("Function -> Start")
    time.sleep(5)
    response = requests.get("http://localhost")
    print(f"Pinging NGINX: {response.status_code}")
    print("Function -> Done")


if __name__ == "__main__":
    print("Main -> start")
    time.sleep(3)
    important_function()
    print("Main -> Done")
