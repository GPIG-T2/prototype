from client import Client


class Model:
    def __init__(self, client: Client) -> None:
        self._client = client

    def tick(self) -> None:
        pass

    @property
    def is_running(self) -> bool:
        # TODO caclulate this on the fly when model is implemented
        return False
