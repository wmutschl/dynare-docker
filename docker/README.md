# Dynare Docker Containers

We provide a range of pre-configured Docker containers for [Dynare](https://www.dynare.org), which include both MATLAB® and GNU Octave (with Dynare already on the search path) and all recommended toolboxes and packages. These containers are ideal for using Dynare in CI/CD environments or on High Performance Computing clusters with [Docker, ENROOT or Singularity/Apptainer](https://wiki.bwhpc.de/e/BwUniCluster2.0/Containers).

To minimize maintenance efforts while ensuring high levels of security, reliability, and performance, our Docker containers are built from the official [MATLAB container base image](https://hub.docker.com/r/mathworks/matlab) using a custom [Dockerfile](Dockerfile). The images are rebuilt every month to pick up updates of the base images, and are tested weekly with the Dynare testsuite, see [wmutschl/dynare-docker](https://github.com/wmutschl/dynare-docker). For more information on building and customizing the containers, see the [build instructions and customization](#build-instructions-and-customization) section below. Additionally, we provide an example [docker-compose file](docker-compose.yml) for complete access to the Ubuntu Desktop via VNC.

## Supported tags

Each image is available under three tags: `X.Y` (e.g. `7.2`), `X.Y-<MATLAB release>` (e.g. `7.2-R2026a`) and a dated snapshot `X.Y-<MATLAB release>-<YYYY-MM-DD>` of each monthly build.

| Tags             | Dynare Version | MATLAB® Version | Octave Version | Operating System | Base Image              |
|------------------|----------------|-----------------|----------------|------------------|-------------------------|
| latest, 7.2      | 7.2            | R2026a          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2026a |
| 7.1              | 7.1            | R2026a          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2026a |
| 7.0              | 7.0            | R2025b          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2025b |
| 6.5              | 6.5            | R2025b          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2025b |
| 6.4              | 6.4            | R2025a          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2025a |
| 6.3              | 6.3            | R2024b          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2024b |
| 6.2              | 6.2            | R2024b          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2024b |
| 6.1              | 6.1            | R2024a          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2024a |
| 6.0              | 6.0            | R2023b          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2023b |
| 5.5              | 5.5            | R2023b          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2023b |
| 5.4              | 5.4            | R2023a          | 8.4.0          | Ubuntu 24.04     | mathworks/matlab:R2023a |
| 5.3              | 5.3            | R2022b          | 5.2.0          | Ubuntu 20.04     | mathworks/matlab:R2022b |
| 5.2              | 5.2            | R2022a          | 5.2.0          | Ubuntu 20.04     | mathworks/matlab:R2022a |
| 5.1              | 5.1            | R2022a          | 5.2.0          | Ubuntu 20.04     | mathworks/matlab:R2022a |
| 5.0              | 5.0            | R2021b          | 5.2.0          | Ubuntu 20.04     | mathworks/matlab:R2021b |
| 4.6.4            | 4.6.4          | R2021a          | 5.2.0          | Ubuntu 20.04     | mathworks/matlab:R2021a |

Dynare 6.x and 7.x images are rebuilt monthly; the 4.6.4 and 5.x images are no longer rebuilt regularly (their Ubuntu 20.04 base images are not updated anymore by MathWorks).
Octave is installed from the official Ubuntu repositories. Octave 8.4.0 (Ubuntu 24.04) is supported by all Dynare 6.x and 7.x releases. For Dynare 7.x, the Octave Forge `datatypes` package (required by Dynare but not packaged in Ubuntu 24.04) is additionally installed from Octave Forge.

## How to interact with the container

To pull the latest image to your machine, execute:
```sh
docker pull dynare/dynare:latest
```
or a specific version:
```sh
docker pull dynare/dynare:7.2
```
In the following we assume that you have access to a MATLAB license and show different workflows how to interact with the container.
Obviously, you need to adjust the environment variable `MLM_LICENSE_FILE` to your use case, please refer to the [MATLAB license](#matlab-license) section on licensing information.
Alternatively, if you don't have access to a license or the closed-source mentality of MATLAB is an irreconcilable issue for you, you can equally well use Dynare with the free and open-source alternative Octave, which needs no license at all.

Note on the entrypoint: the container starts through the entrypoint of the MathWorks base image, which understands the modes `-browser`, `-vnc`, `-shell` and `-help`; **any other arguments are passed to `matlab`** (e.g. `-batch "..."`).
To run another program (Octave, a bash script, ...), override the entrypoint with `--entrypoint`, as shown below.

Where to find the examples: Dynare 7 reorganized its examples into subfolders, e.g. `example1.mod` of Dynare ⩽ 6 is now `examples/stochastic_simulations/collard_2001_theoretical_moments.mod`. The commands below use Dynare 7.

### Run Dynare with Octave in an interactive command prompt

```sh
docker run -it --rm --shm-size=512M --entrypoint octave dynare/dynare:latest
```
and at the Octave prompt:
```matlab
cd /home/matlab/dynare/examples/stochastic_simulations
dynare collard_2001_theoretical_moments
```

### Run Dynare with Octave non-interactively

```sh
docker run --rm --shm-size=512M --entrypoint octave dynare/dynare:latest \
  --eval "cd /home/matlab/dynare/examples/stochastic_simulations; dynare collard_2001_theoretical_moments console nograph"
```

### Run Dynare with MATLAB non-interactively in batch mode

```sh
docker run --rm --shm-size=512M -e MLM_LICENSE_FILE=27000@matlab-campus.uni-tuebingen.de dynare/dynare:latest \
  -batch "cd /home/matlab/dynare/examples/stochastic_simulations; dynare collard_2001_theoretical_moments console"
```

### Run Dynare in an interactive MATLAB session in the browser

```sh
docker run -it --rm -p 8888:8888 -e MLM_LICENSE_FILE=27000@matlab-campus.uni-tuebingen.de --shm-size=512M dynare/dynare:latest -browser
```
You will receive a URL to access MATLAB in a web browser, for example: `http://localhost:8888` or another IP address that you can use to reach your server, such as through a VPN like [Tailscale](https://tailscale.com) if you are behind a firewall. Note that if you set `MLM_LICENSE_FILE` to empty or leave it out from the command, you will be prompted to enter credentials for a MathWorks account associated with a MATLAB license. If you are using a network license manager, switch to the Network License Manager tab and enter the license server address instead. After providing your license information, a MATLAB session will start in the browser. This may take several minutes. To modify the behavior of MATLAB when launched with the `-browser` flag, pass environment variables to the `docker run` command. For more information, see [Advanced Usage](https://github.com/mathworks/matlab-proxy/blob/main/Advanced-Usage.md).

### Run Ubuntu desktop and interact with it via VNC

```sh
docker run -it --rm -p 5901:5901 -p 6080:6080 -e PASSWORD=dynare -e MLM_LICENSE_FILE=27000@matlab-campus.uni-tuebingen.de --shm-size=512M dynare/dynare:latest -vnc
```
To connect to the Ubuntu desktop, either:

- Point a browser to port 6080 of the docker host machine running this container (`http://hostname:6080`).
- Use a VNC client to connect to display 1 of the docker host machine (`hostname:1`). The VNC password is `matlab` by default, you can change that by adjusting the `PASSWORD` environment variable in the run command.
- If you are behind a firewall, we recommend to use a VPN such as [Tailscale](https://tailscale.com) such that you can access the VNC server via the Tailscale address of the server.

The [docker-compose file](docker-compose.yml) starts the container in this mode.

### Run a bash shell inside the container

```sh
docker run -it --rm --shm-size=512M --entrypoint /bin/bash dynare/dynare:latest
```
You can also non-interactively run a sequence of commands:
```sh
docker run --rm --shm-size=512M \
  -e MLM_LICENSE_FILE=27000@matlab-campus.uni-tuebingen.de \
  --entrypoint /bin/bash dynare/dynare:latest -c "\
    cd /home/matlab/dynare/examples/stochastic_simulations && \
    matlab -batch 'dynare collard_2001_theoretical_moments console' && \
    octave --eval 'dynare collard_2001_theoretical_moments console nograph'"
```

### Run MATLAB Desktop using X11

```sh
xhost +
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e MLM_LICENSE_FILE=27000@matlab-campus.uni-tuebingen.de --shm-size=512M dynare/dynare:latest
```
The Desktop window of MATLAB will open on your machine. Note that the command above works only on a Linux operating system with X11 and its dependencies installed.

### Singularity/Apptainer and ENROOT

On HPC clusters your home directory usually replaces the one of the container, so the startup files in `/home/matlab` are not read.
For MATLAB, Dynare is nevertheless on the search path through the `MATLABPATH` environment variable of the image.
For Octave, add the path explicitly, e.g. `octave --eval "addpath /home/matlab/dynare/matlab; dynare mymodel"`.

## Additional information

### MATLAB license

The images contain no license information. To run MATLAB, your license must be [configured for cloud use](https://mathworks.com/help/install/license/licensing-for-mathworks-products-running-on-the-cloud.html). Individual and Campus-Wide licenses are already configured for cloud use. If you have a different license type, please contact your license administrator. If you don't have a MATLAB license, you can obtain a trial license at [MATLAB Trial for Docker](https://www.mathworks.com/campaigns/products/trials/targeted/dkr.html). Octave needs no license.

#### Network license

If you're using a network license manager, pass the port and hostname via the `MLM_LICENSE_FILE` environment variable in your `docker run` command or Docker Compose file:
```sh
docker run --rm --shm-size=512M -e MLM_LICENSE_FILE=27000@matlab-campus.uni-tuebingen.de dynare/dynare:latest \
  -batch "cd /home/matlab/dynare/examples/stochastic_simulations; dynare collard_2001_theoretical_moments console"
```
This is the most robust option for unattended use (CI runners, clusters).

#### Sign in with a MathWorks account (online licensing)

If `MLM_LICENSE_FILE` is not set, MATLAB asks for the credentials of a MathWorks account associated with a license, either in the terminal, in the browser (`-browser`) or on the desktop (`-vnc`).
Since R2023b, this is the default licensing mechanism for Individual and Campus-Wide licenses.

#### License file

For license types that support license files, create a license file via the MathWorks License Center, refer to [Option 2](https://www.mathworks.com/matlabcentral/answers/235126-how-do-i-generate-a-matlab-license-file#answer_190013) for detailed instructions.
For this process, you will need the `username` and a `host ID`. In the container, the username is predefined as `matlab`.
The `host ID` corresponds to the MAC address of any network adapter in the container.
In Docker, you can supply a [randomly generated MAC address](https://miniwebtool.com/mac-address-generator/) (e.g., A6-7E-1A-F4-9A-92) in the `docker run` command.
Download the file from the MathWorks License Center and mount it as a (read-only) volume:
```sh
docker run --rm --mac-address A6-7E-1A-F4-9A-92 --shm-size=512M -v $HOME/matlab-license/:/licenses:ro -e MLM_LICENSE_FILE=/licenses/license.lic dynare/dynare:latest \
  -batch "cd /home/matlab/dynare/examples/stochastic_simulations; dynare collard_2001_theoretical_moments console"
```
Note that since R2023b many individual licenses use online licensing and no longer work with license files.

#### Batch licensing token

For non-interactive environments, MathWorks offers [batch licensing tokens](https://github.com/mathworks-ref-arch/matlab-dockerfile/blob/main/alternates/non-interactive/MATLAB-BATCH.md) that are used with the `matlab-batch` executable (not included in the image, download it from `https://ssd.mathworks.com/supportfiles/ci/matlab-batch/v1/glnxa64/matlab-batch`) and the `MLM_LICENSE_TOKEN` environment variable. `matlab-batch` ignores `startup.m`, but Dynare is on the path anyway through `MATLABPATH`.

### Environment variables

When running the `docker run` command, you can specify environment variables using the `-e` option. The [base image](https://hub.docker.com/r/mathworks/matlab) documentation lists the available variables, such as `MLM_LICENSE_FILE`, `PASSWORD`, or `PROXY_SETTINGS`.

## Build instructions and customization

The images on [Docker Hub](https://hub.docker.com/r/dynare/dynare) are built with (BuildKit is required):
```sh
docker build --build-arg MATLAB_RELEASE=R2026a --build-arg DYNARE_RELEASE=7.2 -t dynare/dynare:7.2 .
docker build --build-arg MATLAB_RELEASE=R2025b --build-arg DYNARE_RELEASE=6.5 -t dynare/dynare:6.5 .
```
The full list of Dynare/MATLAB combinations is maintained in [versions.json](../versions.json).
Useful build arguments besides `DYNARE_RELEASE` and `MATLAB_RELEASE` are `ADDITIONAL_PRODUCTS` (MathWorks products installed with mpm), `SMOKE_TEST=false` (skip the Octave test run at the end of the build) and `LICENSE_SERVER` (bake a network license server into a private image).
Note that `mpm` occasionally crashes with a segmentation fault; the Dockerfile therefore retries the installation once.

If you need to customize the container, there are two ways to do so. You can either adjust the [Dockerfile](Dockerfile) and rebuild the container, or you can run the container interactively, make the necessary adjustments, and then commit the changes for later use with `docker commit`. For more information, see the [Docker documentation](https://docs.docker.com/engine/reference/commandline/commit/) and how to [save changes in the containers](https://www.mathworks.com/help/cloudcenter/ug/save-changes-in-containers.html).

Note that if you plan to distribute your custom container, you should be aware of the licensing terms of any software included in the container.
The provided containers provide no inclusion or information about a MATLAB license file.

## License

This container includes commercial software products from The MathWorks, Inc. ("MathWorks Programs") and related materials. The MathWorks Programs are licensed under the MathWorks Software License Agreement, which is available in the MATLAB installation within this container.

The related materials in this container are licensed under separate licenses, which can be found in their respective folders.

Dynare is licensed under the GPL-3+.
