from typing import Optional

import docker
from docker.client import DockerClient
from docker.models.containers import Container
from docker.errors import NotFound


def get_existing_container(client: DockerClient, name: str) -> Optional[Container]:
    """Gets existing container by name and returns if exists"""
    try:
        container = client.containers.get(name)
        return container
    except NotFound:
        return None


def run_container(image: str, name: str, options: dict, remove_container: bool = True):
    def wrapper(func):
        def decorated(*args, **kwargs):
            container = None
            try:
                client = docker.from_env()
                container = get_existing_container(client, name)
                # If no container is found create a new one, else start existing
                if not container:
                    container = client.containers.run(
                        image,
                        name=name,
                        **options,
                    )
                else:
                    container.start()
                result = func(*args, **kwargs)
                return result
            finally:
                if container is not None:
                    if remove_container:
                        container.remove(force=True)
                    else:
                        container.stop()

        return decorated

    return wrapper
