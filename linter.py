import os
from fastapi import FastAPI
from multiprocessing import Lock
import subprocess
import random

from services_addresses import get_env_or_raise
from schema import LinterRequest, LinterResponse

linter_app = FastAPI()
lock = Lock()

responses_count = 0
linter_path_to_binary = ""


@linter_app.get("/")
def health_check() -> str:
    return "ok linter"


@linter_app.post("/set_binary")
def set_binary(path_to_binary: str) -> None:
    global linter_path_to_binary

    try:
        lock.acquire()
        linter_path_to_binary = path_to_binary
    finally:
        lock.release()


@linter_app.post("/validate")
def validate_file(request: LinterRequest) -> LinterResponse:
    global responses_count

    debug = []
    try:
        lock.acquire()

        responses_count += 1

        if get_env_or_raise("LINTER_DEBUG"):
            debug = [
                f"Current responses_count: {responses_count}",
                f"Current path to linter binary: {linter_path_to_binary}",
            ]
    finally:
        lock.release()

    # We can get a collision with another instance, but I don't think it is important (prob. is low).
    tmp_file_name = f'tmp{random.randint(1, 1000000000)}.txt'
    with open(tmp_file_name, "w") as f:
        f.write(request.code)

    with open(tmp_file_name, "r") as f:
        result = subprocess.run([f"{linter_path_to_binary}"], text=True, stdin=f, stdout=subprocess.PIPE)
    os.remove(tmp_file_name)

    if result.returncode == 0:
        return LinterResponse(result="ok", errors=[], debug=debug)

    errors = result.stdout.strip().split('\n')
    return LinterResponse(result="fail", errors=errors, debug=debug)


print("started linter instance!")
