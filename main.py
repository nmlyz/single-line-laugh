#!/usr/bin/env python3
"""One Line, One Laugh: write a single judged joke line to a text file.

The entry is one line about a dentist visit. The laugh lands in two
beats: the patient answers "emotionally" to a yes-or-no floss question,
and the dentist treats that answer as a clinical finding worth writing
down. The line was the winner of a 38-candidate pairwise tournament
judged against the brief, and it is kept here as a fixed string so the
output never drifts between runs.

What this program does, in order:

1. Assemble the entry from its two spoken beats (question, then answer
   plus the dentist's reaction) and check it against the entry gate:
   1-140 characters, exactly one line, no surrounding whitespace, and
   exactly the judged length of 99 characters.
2. Encode it as UTF-8 with a trailing newline and write it to
   ``entry.txt`` under ``$MAKEFUN_OUTPUT_DIR`` (default ``/output``).
3. Read the file back and compare every byte, then report the byte
   count that was written.

No network access, no randomness, no arguments: the same input always
produces the same bytes.
"""

import hashlib
import os
import sys

# The two beats of the joke, joined with a single space each. Keeping
# them separate makes the turn visible in the source: the setup ends
# with the floss question, the punchline starts with the answer.
SETUP = "My dentist asked if I floss"
PUNCHLINE = "and I said 'emotionally,' and he wrote it down like it was a diagnosis."

ENTRY = SETUP + " " + PUNCHLINE

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 140
JUDGED_CHARS = 99
OUTPUT_NAME = "entry.txt"
FILE_MODE = 0o644


def gate_problems(line):
    """Return a list of every entry-gate rule the line breaks (empty = pass)."""
    problems = []
    if not GATE_MIN_CHARS <= len(line) <= GATE_MAX_CHARS:
        problems.append(
            "length %d is outside the %d-%d character gate"
            % (len(line), GATE_MIN_CHARS, GATE_MAX_CHARS)
        )
    if len(line) != JUDGED_CHARS:
        problems.append(
            "length %d does not match the judged length of %d"
            % (len(line), JUDGED_CHARS)
        )
    if "\n" in line or "\r" in line:
        problems.append("entry must be exactly one line")
    if line != line.strip():
        problems.append("entry must not start or end with whitespace")
    if "  " in line:
        problems.append("entry must not contain a double space")
    return problems


def encode_entry(line):
    """Turn the judged line into the exact bytes written to disk."""
    return (line + "\n").encode("utf-8")


def output_path():
    """Resolve the destination file from the environment, with a default."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, OUTPUT_NAME)


def write_entry(path, payload):
    """Write the payload, creating the output directory if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(payload)
    os.chmod(path, FILE_MODE)


def read_back(path):
    """Return the raw bytes currently stored at the destination."""
    with open(path, "rb") as handle:
        return handle.read()


def verify_bytes(stored, payload):
    """Byte-level check: the file must hold exactly the payload."""
    if stored != payload:
        return "read-back mismatch: %d bytes on disk, %d bytes expected" % (
            len(stored),
            len(payload),
        )
    return None


def verify_checksum(stored, payload):
    """Second, independent check: SHA-256 of file vs payload must match."""
    if hashlib.sha256(stored).hexdigest() != hashlib.sha256(payload).hexdigest():
        return "checksum mismatch after write"
    return None


def verify_entry(path, payload):
    """Confirm the file on disk is byte-identical to what was written.

    Two independent checks run in sequence so a silent partial write
    cannot slip through: an exact byte comparison, then a digest
    comparison over the same bytes.
    """
    stored = read_back(path)
    for check in (verify_bytes, verify_checksum):
        failure = check(stored, payload)
        if failure is not None:
            return failure
    return None


def check_only():
    """Validate the entry against the gate without writing anything."""
    problems = gate_problems(ENTRY)
    if problems:
        for problem in problems:
            print("gate failed: " + problem, file=sys.stderr)
        return 1
    print("entry OK: %d characters, one line" % len(ENTRY))
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv == ["--check"]:
        sys.exit(check_only())
    if argv:
        print("usage: main.py [--check]", file=sys.stderr)
        sys.exit(2)
    problems = gate_problems(ENTRY)
    if problems:
        for problem in problems:
            print("gate failed: " + problem, file=sys.stderr)
        sys.exit(1)
    payload = encode_entry(ENTRY)
    path = output_path()
    write_entry(path, payload)
    failure = verify_entry(path, payload)
    if failure is not None:
        print(failure, file=sys.stderr)
        sys.exit(1)
    print("wrote %d bytes to %s" % (len(payload), path))


if __name__ == "__main__":
    main()
