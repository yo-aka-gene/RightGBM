import subprocess
from typing import List
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch: str, files_to_edit: List[str]) -> None:
        self.file_to_watch = file_to_watch
        self.files_to_edit = files_to_edit

    def on_modified(self, event) -> None:
        if (
            event.event_type == 'modified'
        ) and (
            event.src_path == self.file_to_watch
        ):
            print(
                f"Update detected in {event.src_path}.\nAutomatically sync files as such."
            )
            for file in self.files_to_edit:
                subprocess.call(f"poetry export --with dev -f requirements.txt -o {file}")

if __name__ == "__main__":
    event_handler = MyHandler(
        file_to_watch="./poetry.lock",
        files_to_edit=[
            "./sandbox/config/requirements.txt",
            "./docs/docs/requirements.txt"
        ]
    )
    observer = Observer()

    # path of directory to watch (= current directory)
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
