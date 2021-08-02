from threading import Event, Thread


class StoppableThread(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()
