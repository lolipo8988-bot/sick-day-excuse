#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry line for 'The Funniest Sick-Day Excuse' to /output/entry.txt.

The competition asks for one single line of under 200 characters: the
funniest sick-day excuse someone could send to call in sick, and
nothing else. The gate checks that /output/entry.txt is UTF-8 text of
1 to 200 characters and not only white space.

The output path defaults to /output/entry.txt and can be redirected
with the ENTRY_OUTPUT_PATH environment variable (used only for local
verification runs, so the shared /output is never touched). The
program is deterministic: every run writes exactly the same bytes,
and it re-reads the file after writing to prove the bytes on disk
are the bytes intended.
"""

import os

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
OUTPUT_ENV_VAR = "ENTRY_OUTPUT_PATH"
MAX_CHARS = 200

# The excuse, revised after the first run. The draft explained the
# Face ID idea flatly ("does not recognize my face... until I look
# like myself again"); the final line sharpens the setup to "swollen
# and congested" (a sickness a boss half believes), lets Face ID
# "keep rejecting" the narrator like a bouncer, and moves the
# funniest idea to the very end: recovery as re-authorization --
# you have to get better before you are authorized to be yourself
# again. No worn fever, dog or grandmother material, and every
# clause either sets up the sickness or loads the last line.
ENTRY_PARTS = (
    "Can't come in today — I'm so swollen and congested that Face ID "
    "keeps rejecting me. ",
    "Apparently I have to get better before I'm authorized to be myself again.",
)


def build_entry() -> str:
    """Assemble the one-line excuse and hold it to the gate's rules."""
    text = "".join(ENTRY_PARTS)
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1..{MAX_CHARS} characters, got {len(text)}"
    )
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert text.strip(), "entry must not be only white space"
    return text


def write_entry(text: str, output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(output_path, "rb") as f:
        on_disk = f.read()
    assert on_disk == text.encode("utf-8"), "bytes on disk differ from entry"


def main() -> None:
    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)
    write_entry(build_entry(), output_path)


if __name__ == "__main__":
    main()
