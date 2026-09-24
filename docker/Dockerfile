# syntax=docker/dockerfile:1
# Copyright © 2023-2026 Dynare Team
#
# This file is part of Dynare.
#
# Dynare is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dynare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dynare.  If not, see <https://www.gnu.org/licenses/>.

##############################################################################################################
# INFORMATION:                                                                                               #
# This Dockerfile installs Dynare (https://dynare.org)                                                       #
#  - with MATLAB including the following toolboxes (https://github.com/mathworks-ref-arch/matlab-dockerfile) #
#    MATLAB Symbolic_Math_Toolbox Statistics_and_Machine_Learning_Toolbox Optimization_Toolbox               #
#    Econometrics_Toolbox Parallel_Computing_Toolbox Control_System_Toolbox Global_Optimization_Toolbox      #
#  - with Octave including the following packages (using Ubuntu packages):                                   #
#    octave-control octave-econometrics octave-io octave-statistics octave-struct octave-parallel            #
#    NOTE: Dynare >= 7 needs the Octave "datatypes" package, which requires Octave >= 9.1.0 and is not       #
#    available for the Octave 8.4.0 of Ubuntu 24.04. Hence Dynare 7.x can only be used with MATLAB in these  #
#    images; use the Octave-only images (Dockerfile.octave, tags X.Y-octave) for Dynare 7.x with Octave.     #
# It also renames the GCC libraries of MATLAB (similar to the matlab-support package) to avoid conflicts     #
# with the system libraries and puts Dynare on the MATLAB and Octave search paths.                           #
#                                                                                                            #
# MATLAB LICENSE:                                                                                            #
# The container is created without any information on a license. To use Dynare with MATLAB, you need to     #
# provide a valid license at runtime, see README.md#matlab-license. Octave needs no license.                 #
##############################################################################################################

# DYNARE_RELEASE must be a tag on https://git.dynare.org/dynare/dynare
#   Dynare >= 6 uses the meson build system, Dynare 4.x and 5.x use autoconf/automake.
# MATLAB_RELEASE must be a tag on https://hub.docker.com/r/mathworks/matlab/tags
#   R2023a and newer base images run Ubuntu 24.04 (Octave 8.4.0, GCC 13, meson 1.3.2),
#   R2021a to R2022b base images run Ubuntu 20.04 (Octave 5.2.0) and are only suitable for Dynare 4.x/5.x.
# The version matrix that is actually built lives in versions.json at the root of the dynare-docker repository.
#
# Dynare compatibility (from the release announcements in NEWS.md):
# - 7.2              : MATLAB R2020a to R2026a, Octave 8.4.0 to 11.3.0
# - 7.1 (2026-05-28) : MATLAB R2020a to R2026a, Octave 8.4.0 to 11.1.0
# - 7.0 (2026-03-19) : MATLAB R2020a to R2025b, Octave 8.4.0 to 11.1.0
# - 6.5 (2025-11-24) : MATLAB R2018b to R2025b, Octave 7.1.0 to 10.3.0
# - 6.4 (2025-06-26) : MATLAB R2018b to R2025a, Octave 7.1.0 to 10.2.0
# - 6.3 (2025-02-19) : MATLAB R2018b to R2024b, Octave 7.1.0 to 9.4.0
# - 6.2 (2024-09-25) : MATLAB R2018b to R2024b, Octave 7.1.0 to 9.2.0
# - 6.1 (2024-05-02) : MATLAB R2018b to R2024a, Octave 7.1.0 to 9.1.0
# - 6.0 (2024-02-02) : MATLAB R2018b to R2023b, Octave 7.1.0 to 8.4.0

ARG MATLAB_RELEASE=R2026a
ARG DYNARE_RELEASE=7.2

# Specify the base image with pre-installed MATLAB
FROM mathworks/matlab:${MATLAB_RELEASE}

# Re-declare the global arguments to use them in this build stage
ARG MATLAB_RELEASE
ARG DYNARE_RELEASE

# Specify the list of products to install into MATLAB with mpm
ARG ADDITIONAL_PRODUCTS="Symbolic_Math_Toolbox Statistics_and_Machine_Learning_Toolbox Optimization_Toolbox Econometrics_Toolbox Parallel_Computing_Toolbox Control_System_Toolbox Global_Optimization_Toolbox"

# Specify the fonts packages to install into the image. The default value below installs fonts for ja_JP-UTF-8 locales support.
ARG FONTS_PACKAGES="fonts-vlgothic ibus-mozc"

# Specify extra Ubuntu APT packages to install into the image
ARG ADDITIONAL_APT_PACKAGES="unzip"

# MATLAB install location of the base image
ARG MATLAB_INSTALL_LOCATION="/opt/matlab/${MATLAB_RELEASE}"

# Run a quick Dynare example with Octave at the end of the build (needs no license)
ARG SMOKE_TEST=true

# Optional license server (port@hostname) baked into the image; leave empty for public images
ARG LICENSE_SERVER

LABEL org.opencontainers.image.title="Dynare" \
      org.opencontainers.image.description="Dynare with MATLAB and Octave for macroeconomic modeling" \
      org.opencontainers.image.url="https://www.dynare.org" \
      org.opencontainers.image.source="https://github.com/wmutschl/dynare-docker" \
      org.opencontainers.image.vendor="Dynare Team" \
      org.opencontainers.image.licenses="GPL-3.0-or-later" \
      dynare.version="${DYNARE_RELEASE}" \
      matlab.version="${MATLAB_RELEASE}"

# By default, the MATLAB container runs as user "matlab". To install packages, switch to root.
USER root

# Install mpm dependencies
RUN <<'EOF'
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install --no-install-recommends --yes \
    wget \
    ca-certificates \
    ${FONTS_PACKAGES} \
    ${ADDITIONAL_APT_PACKAGES}
apt-get clean
apt-get autoremove --yes
rm -rf /var/lib/apt/lists/*
EOF

# Run mpm to install additional MathWorks products into the existing MATLAB installation directory,
# and delete mpm afterwards. If mpm fails, print its logfile.
# mpm is run as user matlab (with sudo) and $HOME passed in, so that support packages end up in the right place.
# Hint: mpm occasionally crashes with a segmentation fault; the install is therefore attempted twice.
WORKDIR /tmp
USER matlab
RUN <<'EOF'
set -e
wget -q https://www.mathworks.com/mpm/glnxa64/mpm
chmod +x mpm
EXISTING_MATLAB_LOCATION=$(dirname "$(dirname "$(readlink -f "$(which matlab)")")")
for attempt in 1 2; do
    if sudo HOME=${HOME} ./mpm install \
        --destination="${EXISTING_MATLAB_LOCATION}" \
        --release="${MATLAB_RELEASE}" \
        --products ${ADDITIONAL_PRODUCTS}; then
        sudo rm -rf mpm /tmp/mathworks_root.log
        exit 0
    fi
    echo "MPM installation attempt ${attempt} failed. See below for more information:"
    sudo cat /tmp/mathworks_root.log || true
done
exit 1
EOF

USER root

# Install the dependencies of Dynare and keep this layer small (apt cache cleanup)
RUN <<'EOF'
set -e
export DEBIAN_FRONTEND=noninteractive

# R2021a to R2022b base images run Ubuntu 20.04 (liboctave-dev), newer ones run Ubuntu 24.04 (octave-dev)
case "${MATLAB_RELEASE}" in
    R2021a|R2021b|R2022a|R2022b) OCTAVE_DEV_PKG="liboctave-dev" ;;
    *)                           OCTAVE_DEV_PKG="octave-dev" ;;
esac

# Build system: autotools for Dynare 4.x/5.x, meson for Dynare >= 6
case "${DYNARE_RELEASE}" in
    4.*|5.*) BUILD_SYSTEM_PKGS="build-essential autoconf automake doxygen" ;;
    *)       BUILD_SYSTEM_PKGS="gcc g++ meson pkgconf" ;;
esac

apt-get update
apt-get install --no-install-recommends --yes \
    ${BUILD_SYSTEM_PKGS} \
    gfortran \
    flex \
    libfl-dev \
    bison \
    git \
    git-lfs \
    libboost-graph-dev \
    libgsl-dev \
    libmatio-dev \
    libslicot-dev \
    libslicot-pic \
    libsuitesparse-dev \
    texlive \
    texlive-publishers \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-font-utils \
    texlive-latex-recommended \
    texlive-science \
    texlive-plain-generic \
    lmodern \
    cm-super \
    python3-sphinx \
    tex-gyre \
    latexmk \
    libjs-mathjax \
    x13as \
    ${OCTAVE_DEV_PKG} \
    octave-control \
    octave-econometrics \
    octave-io \
    octave-statistics \
    octave-struct \
    octave-parallel \
    gnuplot \
    fonts-freefont-otf \
    ghostscript \
    epstool
apt-get clean
apt-get autoremove --yes
rm -rf /var/lib/apt/lists/*
EOF

# The MathWorks base images symlink /usr/bin/gcc and /usr/bin/g++ to gcc-12/g++-12 (the MEX compiler of MATLAB).
# Dynare >= 7 requires GCC >= 13, so make sure the default compilers are the ones of the distribution.
RUN <<'EOF'
set -e
case "${DYNARE_RELEASE}" in
    4.*|5.*) exit 0 ;;
esac
for tool in gcc g++ gfortran; do
    major=$(${tool} -dumpversion | cut -d. -f1)
    if [ "${major}" -lt 13 ]; then
        if [ -x "/usr/bin/${tool}-13" ]; then
            ln -sf "${tool}-13" "/usr/bin/${tool}"
            echo "Pointed /usr/bin/${tool} to ${tool}-13 (was version ${major})"
        else
            echo "Error: ${tool} version ${major} is too old and ${tool}-13 is not installed"
            exit 1
        fi
    fi
    echo "${tool}: $(${tool} -dumpfullversion)"
done
EOF

# Dynare >= 7 requires the Octave "datatypes" package. Every release of it requires Octave >= 9.1.0, so it cannot be
# installed with the Octave 8.4.0 of Ubuntu 24.04 (releases 1.0.1-1.0.9 and 1.2.0 were tried). Install the distribution
# package if the base image provides it (newer Ubuntu releases), otherwise mark Octave as unsupported in this image.
RUN <<'EOF'
set -e
case "${DYNARE_RELEASE}" in
    4.*|5.*|6.*) exit 0 ;;
esac
export DEBIAN_FRONTEND=noninteractive
apt-get update
if apt-cache show octave-datatypes > /dev/null 2>&1; then
    apt-get install --no-install-recommends --yes octave-datatypes
else
    OCTAVE_VERSION=$(octave --no-gui --no-init-file --eval "disp(version)" 2>/dev/null | tail -n 1)
    echo "Warning: Dynare ${DYNARE_RELEASE} cannot be used with Octave ${OCTAVE_VERSION} in this image (the datatypes package needs Octave >= 9.1.0). Use MATLAB or the dynare/dynare:${DYNARE_RELEASE}-octave image." \
        | tee /etc/dynare-octave-unsupported
fi
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF

# Rename the GCC libraries shipped with MATLAB to avoid conflicts with the system libraries
# (see the matlab-support package: https://salsa.debian.org/debian/matlab-support/-/blob/master/debian/matlab-support.postinst)
# libtiff.so.5 is renamed as well to fix epstopdf LaTeX errors (LIBTIFF_4.0 not found)
RUN <<'EOF'
set -e
for lib in \
    "${MATLAB_INSTALL_LOCATION}/sys/os/glnxa64/libgcc_s.so.1" \
    "${MATLAB_INSTALL_LOCATION}/sys/os/glnxa64/libstdc++.so.6" \
    "${MATLAB_INSTALL_LOCATION}/sys/os/glnxa64/libgfortran.so.5" \
    "${MATLAB_INSTALL_LOCATION}/sys/os/glnxa64/libquadmath.so.0" \
    "${MATLAB_INSTALL_LOCATION}/bin/glnxa64/libfreetype.so.6" \
    "${MATLAB_INSTALL_LOCATION}/bin/glnxa64/libtiff.so.5"; do
    if [ -f "${lib}" ]; then
        mv "${lib}" "${lib}.bak"
        echo "Renamed: ${lib}"
    fi
done
EOF

# No license is included in the image. A license server can be baked in with --build-arg LICENSE_SERVER=port@hostname,
# but for public images this must stay empty: pass MLM_LICENSE_FILE (or MLM_LICENSE_TOKEN) at runtime instead.
ENV MLM_LICENSE_FILE=${LICENSE_SERVER}

# Get and compile the Dynare sources as user matlab
USER matlab
WORKDIR /home/matlab
RUN git lfs install \
    && git clone --depth 1 --branch ${DYNARE_RELEASE} --recurse-submodules https://git.dynare.org/dynare/dynare.git

RUN <<'EOF'
set -e
cd /home/matlab/dynare
case "${DYNARE_RELEASE}" in
    4.*|5.*)
        # Autotools build system (Dynare 4.x/5.x)
        autoreconf -si
        ./configure --with-matlab=${MATLAB_INSTALL_LOCATION} MATLAB_VERSION=${MATLAB_RELEASE}
        make -j$(($(nproc)+1))
        ;;
    *)
        # Meson build system (Dynare >= 6)
        meson setup -Dmatlab_path=${MATLAB_INSTALL_LOCATION} -Dbuildtype=debugoptimized build-matlab
        meson compile -C build-matlab
        meson setup -Dbuild_for=octave -Dbuildtype=debugoptimized build-octave
        meson compile -C build-octave
        ;;
esac
EOF

# Put Dynare on the search paths of MATLAB and Octave.
# MATLABPATH also works for matlab-batch (which ignores startup.m) and when $HOME is replaced
# (e.g. Singularity/Apptainer on HPC clusters); startup.m is kept for backwards compatibility.
# Octave uses .octaverc (OCTAVE_PATH is not used, as it triggers many "shadows a built-in function" warnings
# on every start, even with --no-init-file).
ENV MATLABPATH=/home/matlab/dynare/matlab
RUN echo "addpath /home/matlab/dynare/matlab" >> /home/matlab/.octaverc

# startup.m of the MathWorks base image is a MATLAB function ending with "end", so insert the addpath before it
USER root
RUN <<'EOF'
set -e
STARTUP_FILE="/home/matlab/Documents/MATLAB/startup.m"
ADDPATH_CMD="addpath('/home/matlab/dynare/matlab');"
mkdir -p "$(dirname "${STARTUP_FILE}")"
if [ -f "${STARTUP_FILE}" ] && [ "$(tail -n 1 "${STARTUP_FILE}" | tr -d '[:space:]')" = "end" ]; then
    sed -i "\$i ${ADDPATH_CMD}" "${STARTUP_FILE}"
else
    echo "${ADDPATH_CMD}" >> "${STARTUP_FILE}"
fi
chown matlab:matlab "${STARTUP_FILE}"
EOF

# Smoke test: run a small example with Octave (no license needed)
USER matlab
RUN <<'EOF'
set -e
if [ "${SMOKE_TEST}" != "true" ]; then
    exit 0
fi
if [ -f /etc/dynare-octave-unsupported ]; then
    cat /etc/dynare-octave-unsupported
    echo "Skipping the Octave smoke test"
    exit 0
fi
cd /home/matlab/dynare/examples
# example1.mod was moved and renamed to stochastic_simulations/collard_2001_theoretical_moments.mod in Dynare 7
MODFILE=$(find . \( -name example1.mod -o -name collard_2001_theoretical_moments.mod \) | head -n 1)
if [ -z "${MODFILE}" ]; then
    echo "Warning: no example found for the smoke test, skipping it"
    exit 0
fi
SMOKE_DIR=$(mktemp -d)
cp "${MODFILE}" "${SMOKE_DIR}/"
cd "${SMOKE_DIR}"
octave --no-gui --eval "dynare $(basename "${MODFILE}") console nograph"
cd /home/matlab
rm -rf "${SMOKE_DIR}"
EOF

# Set user and work directory; ENTRYPOINT and CMD are inherited from the base image
USER matlab
WORKDIR /home/matlab
