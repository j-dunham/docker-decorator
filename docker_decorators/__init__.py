import docker


def run_container(image: str, name: str, options: dict):
    def wrapper(func):
        def decorated(*args, **kwargs):
            container = None
            try:
                client = docker.from_env()
                container = client.containers.run(
                    image,
                    name=name,
                    **options,
                )
                result = func(*args, **kwargs)
                return result
            finally:
                if container is not None:
                    container.remove(force=True)

        return decorated

    return wrapper
