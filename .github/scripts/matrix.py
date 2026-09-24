#!/usr/bin/env python3
"""Compute GitHub Actions matrices from versions.json.

Usage:
    matrix.py build      <selection>
    matrix.py test       <selection> <suites>
    matrix.py installers <selection> <platforms>

<selection> is one of:
    monthly   entries with "schedule": "monthly" (default for scheduled runs)
    all       every entry
    latest    the entries flagged with "latest": true
    list      comma-separated items:
                X.Y          Dynare version X.Y (MATLAB-based and Octave-only images, or installers)
                X.Y-RYYYYx   MATLAB-based image with a specific MATLAB release, possibly a combination
                             not listed in versions.json (tagged X.Y-RYYYYx only, never X.Y or latest)
                X.Y-octave   only the Octave-only image
<suites> is "both", "octave" or "matlab" (test matrix only).
<platforms> is "all", "windows" or "macos" (installers matrix only).

The matrix is printed as JSON on stdout, for use with fromJSON() in a workflow.
"""

import json
import sys
from datetime import date
from pathlib import Path

VERSIONS_FILE = Path(__file__).resolve().parents[2] / "versions.json"
REPO = "dynare/dynare"


def load():
    data = json.loads(VERSIONS_FILE.read_text())
    entries = [dict(e, variant="matlab") for e in data.get("images", [])]
    entries += [dict(e, variant="octave") for e in data.get("octave_images", [])]
    return entries, data.get("installers", [])


def select(entries, selection):
    selection = selection.strip() or "monthly"
    if selection == "all":
        return entries
    if selection == "monthly":
        return [e for e in entries if e.get("schedule") == "monthly"]
    if selection == "latest":
        return [e for e in entries if e.get("latest")]
    selected = []
    for item in (s.strip() for s in selection.split(",") if s.strip()):
        dynare, _, suffix = item.partition("-")
        matches = [e for e in entries if e["dynare"] == dynare]
        if not matches:
            sys.exit(f"Dynare version {dynare} is not listed in {VERSIONS_FILE.name}")
        if not suffix:
            selected += matches
        elif suffix == "octave":
            octave = [e for e in matches if e["variant"] == "octave"]
            if not octave:
                sys.exit(f"There is no Octave-only image for Dynare {dynare} in {VERSIONS_FILE.name}")
            selected += octave
        else:
            base = [e for e in matches if e.get("variant", "matlab") == "matlab" and "matlab" in e]
            if not base:
                sys.exit(f"There is no MATLAB entry for Dynare {dynare} in {VERSIONS_FILE.name}")
            entry = dict(base[0])
            if suffix != entry["matlab"]:
                # Extra combination: never tag it as the default X.Y or latest
                entry.update(matlab=suffix, latest=False, extra=True)
            selected.append(entry)
    return selected


def image_name(e):
    if e["variant"] == "octave":
        return f"{REPO}:{e['dynare']}-octave"
    return f"{REPO}:{e['dynare']}-{e['matlab']}"


def build_matrix(entries):
    today = date.today().isoformat()
    include = []
    for e in entries:
        dynare = e["dynare"]
        if e["variant"] == "octave":
            tags = [f"{REPO}:{dynare}-octave", f"{REPO}:{dynare}-octave-{today}"]
            if e.get("latest"):
                tags.append(f"{REPO}:latest-octave")
            include.append({
                "name": f"Dynare {dynare} (Octave {e['octave']}, Ubuntu {e['ubuntu']})",
                "dynare": dynare,
                "file": "docker/Dockerfile.octave",
                "build_args": f"DYNARE_RELEASE={dynare}\nUBUNTU_RELEASE={e['ubuntu']}",
                "tags": ",".join(tags),
            })
        else:
            matlab = e["matlab"]
            tags = [f"{REPO}:{dynare}-{matlab}", f"{REPO}:{dynare}-{matlab}-{today}"]
            if not e.get("extra"):
                tags.insert(0, f"{REPO}:{dynare}")
            if e.get("latest"):
                tags.append(f"{REPO}:latest")
            include.append({
                "name": f"Dynare {dynare} (MATLAB {matlab})",
                "dynare": dynare,
                "file": "docker/Dockerfile",
                "build_args": f"DYNARE_RELEASE={dynare}\nMATLAB_RELEASE={matlab}",
                "tags": ",".join(tags),
            })
    return include


def test_matrix(entries, suites):
    suites = ["octave", "matlab"] if suites == "both" else [suites]
    include = []
    for e in entries:
        if e["variant"] == "octave":
            runs = ["octave"]
        else:
            runs = ["matlab"]
            if e.get("octave_supported", True):
                runs.insert(0, "octave")
        for suite in runs:
            if suite not in suites:
                continue
            label = f"Octave {e['octave']}" if suite == "octave" else f"MATLAB {e['matlab']}"
            if e["variant"] == "octave":
                label += f", Ubuntu {e['ubuntu']}"
            include.append({
                "name": f"Dynare {e['dynare']} ({label})",
                "dynare": e["dynare"],
                "suite": suite,
                "image": image_name(e),
                "excludes": " ".join(e.get("test_excludes", {}).get(suite, [])),
                "artifact": image_name(e).split(":")[1] + ("" if e["variant"] == "octave" else f"-{suite}"),
            })
    return include


def installers_matrix(installers, selection, platforms):
    entries = [dict(e, variant="installer") for e in installers]
    entries = select(entries, selection)
    platforms = ["windows", "macos"] if platforms == "all" else [platforms]
    include = []
    for e in entries:
        for platform in platforms:
            include.append({
                "dynare": e["dynare"],
                "matlab": e["matlab"],
                "octave_windows": e.get("octave_windows", ""),
                "platform": platform,
                "runner": "windows-latest" if platform == "windows" else "macos-latest",
            })
    return include


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("build", "test", "installers"):
        sys.exit(__doc__)
    mode, selection = sys.argv[1], sys.argv[2]
    entries, installers = load()
    if mode == "installers":
        include = installers_matrix(installers, selection, sys.argv[3] if len(sys.argv) > 3 else "all")
    elif mode == "build":
        include = build_matrix(select(entries, selection))
    else:
        include = test_matrix(select(entries, selection), sys.argv[3] if len(sys.argv) > 3 else "both")
    print(json.dumps({"include": include}))


if __name__ == "__main__":
    main()
