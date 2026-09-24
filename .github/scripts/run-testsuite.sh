#!/bin/bash
# Runs the Dynare testsuite inside a dynare/dynare container.
# Usage: run-testsuite.sh <matlab|octave> [space-separated test names to exclude]
# Logs are copied to /home/matlab/artifacts (mounted from the host).
set -uo pipefail

suite=$1
excludes=${2:-}
artifacts=/home/matlab/artifacts
mkdir -p "${artifacts}"
cd /home/matlab/dynare || exit 1

if [ -f meson.build ]; then
    # Dynare >= 6: meson testsuite
    build_dir=build-${suite}
    if [ -n "${excludes}" ]; then
        # Run every test listed by meson (which respects the default test setup), except the excluded ones.
        # Test names are printed as "project:suite / name".
        mapfile -t all_tests < <(meson test -C "${build_dir}" --list 2>/dev/null | sed 's|^.* / ||')
        selected=()
        for t in "${all_tests[@]}"; do
            skip=false
            for x in ${excludes}; do
                if [ "${t}" = "${x}" ]; then skip=true; fi
            done
            if [ "${skip}" = true ]; then echo "Excluding test: ${t}"; else selected+=("${t}"); fi
        done
        meson test -C "${build_dir}" --num-processes "$(nproc)" --print-errorlogs "${selected[@]}"
    else
        meson test -C "${build_dir}" --num-processes "$(nproc)" --print-errorlogs
    fi
    rc=$?
    cp "${build_dir}/meson-logs/testlog.txt" "${artifacts}/" 2>/dev/null
else
    # Dynare 4.x/5.x: autotools testsuite
    if [ -n "${excludes}" ]; then
        echo "Warning: test excludes are not supported for the autotools testsuite, ignoring: ${excludes}"
    fi
    cd tests || exit 1
    make check-"${suite}" -j"$(nproc)"
    rc=$?
    ext=${suite:0:1} # .m.log/.m.trs for MATLAB, .o.log/.o.trs for Octave
    find . -type f \( -name "*.${ext}.log" -o -name "*.${ext}.trs" -o -name '*.jnl' \) \
        -exec sh -c 'mkdir -p "$1/$(dirname "$2")" && cp "$2" "$1/$2"' _ "${artifacts}" {} \;
    cp "run_test_${suite}_output.txt" "${artifacts}/" 2>/dev/null
fi

exit ${rc}
