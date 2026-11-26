"""The funniest AI excuse, one line, for make.fun.

The excuse is an agent that did not fail at all: it handed the task
down to a smaller model, which handed it down again, and the smallest
model is now on vacation. This program writes exactly that excuse to
entry.txt, and nothing else.

To stay byte-identical on every run the excuse is a fixed string, and
the file is written with no trailing newline.
"""

import hashlib
import os

# The excuse. One line, plain ASCII, 135 characters.
EXCUSE = "I didn't fail the task. I outsourced it to a smaller model, who outsourced it to an even smaller model, who is now on vacation."


def screen(excuse):
    """Turn away anything the sealed scorer would refuse."""
    total = len(excuse)
    if total < 1 or total > 200:
        raise ValueError("entry must be 1-200 characters, got %d" % total)
    if not excuse.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in excuse or "\r" in excuse:
        raise ValueError("entry must be a single line")
    return excuse


def locate():
    """Decide where the grader wants the entry file to land."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "entry.txt")


def commit(path, excuse):
    """Encode the excuse as UTF-8 and write it, no trailing newline."""
    payload = screen(excuse).encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)
    return payload


def audit(path, payload):
    """Read the file back and confirm it holds exactly the excuse."""
    with open(path, "rb") as handle:
        stored = handle.read()
    assert stored == payload, "entry.txt bytes differ from the excuse"
    assert stored.decode("utf-8") == EXCUSE, "entry.txt text differs from the excuse"
    assert stored == stored.rstrip(), "entry.txt ends with whitespace"


def launch():
    path = locate()
    payload = commit(path, EXCUSE)
    audit(path, payload)
    print(path)
    print(len(payload))
    print(hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    launch()
