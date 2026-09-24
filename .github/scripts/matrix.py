#!/usr/bin/env python3
"""Compute the GitHub Actions matrix from versions.json.

Usage:
    matrix.py build <selection>
    matrix.py test  <selection> <suites>

<selection> is one of:
    monthly   entries with "schedule": "monthly" (default for scheduled runs)
    all       every entry
    latest    the entry flagged with "latest": true
    X.Y[,..]  a comma-separated list of Dynare versions, optionally with a MATLAB release,
              e.g. "7.2" or "6.1-R2023b" (the latter builds a combination not listed in versions.json)
<suites> is "both", "octave" or "matlab" (test matrix only).

The matrix is printed as JSON on stdout, e.g. for use with fromJSON() in a workflow.
"""

import json
import sys
from datetime import date
from pathlib import Path

VERSIONS_FILE = Path(__file__).resolve().parents[2] / "versions.json"


def select(images, selection):
    selection = selection.strip() or "monthly"
    if selection == "all":
        return images
    if selection == "monthly":
        return [i for i in images if i.get("schedule") == "monthly"]
    if selection == "latest":
        return [i for i in images if i.get("latest")]
    selected = []
    for item in (s.strip() for s in selection.split(",") if s.strip()):
        dynare, _, matlab = item.partition("-")
        matches = [i for i in images if i["dynare"] == dynare]
        if not matches:
            sys.exit(f"Dynare version {dynare} is not listed in {VERSIONS_FILE.name}")
        entry = dict(matches[0])
        if matlab:
            if matlab != entry["matlab"]:
                # Extra combination: never tag it as the default X.Y or latest
                entry["latest"] = False
                entry["extra"] = True
            entry["matlab"] = matlab
        selected.append(entry)
    return selected


def image_tags(entry, today):
    repo = "dynare/dynare"
    dynare, matlab = entry["dynare"], entry["matlab"]
    tags = [f"{repo}:{dynare}-{matlab}", f"{repo}:{dynare}-{matlab}-{today}"]
    if not entry.get("extra"):
        tags.insert(0, f"{repo}:{dynare}")
    if entry.get("latest"):
        tags.append(f"{repo}:latest")
    return tags


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("build", "test"):
        sys.exit(__doc__)
    mode, selection = sys.argv[1], sys.argv[2]
    images = json.loads(VERSIONS_FILE.read_text())["images"]
    entries = select(images, selection)
    today = date.today().isoformat()

    include = []
    if mode == "build":
        for e in entries:
            include.append({
                "dynare": e["dynare"],
                "matlab": e["matlab"],
                "tags": ",".join(image_tags(e, today)),
            })
    else:
        suites = sys.argv[3] if len(sys.argv) > 3 else "both"
        suites = ["octave", "matlab"] if suites == "both" else [suites]
        for e in entries:
            for suite in suites:
                include.append({
                    "dynare": e["dynare"],
                    "matlab": e["matlab"],
                    "octave": e.get("octave", ""),
                    "suite": suite,
                    "image": f"dynare/dynare:{e['dynare']}-{e['matlab']}",
                    "excludes": " ".join(e.get("test_excludes", {}).get(suite, [])),
                })
    print(json.dumps({"include": include}))


if __name__ == "__main__":
    main()
