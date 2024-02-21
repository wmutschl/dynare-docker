# Dynare Docker Containers
[Dynare](https://www.dynare.org) is a free software suite designed for analyzing and solving dynamic economic models. It can perform simulations, estimation, forecasting, and policy analysis. 
The Dynare team provides Docker containers for running Dynare on both MATLAB and Octave and publishes them on [Docker Hub](https://hub.docker.com/r/dynare/dynare). For more details on the containers, visit the [Dynare Docker Guide](https://git.dynare.org/Dynare/dynare/-/blob/master/scripts/docker/README.md).

This repository automates the building, pushing and testing of Dynare Docker containers using GitHub Actions workflows.

## Docker builds

The [Dockerfile](https://git.dynare.org/Dynare/dynare/-/raw/master/scripts/docker/Dockerfile) is curled directly from the master branch of the [Dynare GitLab repository](https://git.dynare.org/Dynare/dynare) and is used to build the Docker containers. The containers are then tagged and pushed to [Docker Hub](https://hub.docker.com/r/dynare/dynare). This process is automated to run on every 21st day of the month.

Click on the badges for real-time status reports of the latest builds.

| Dynare 6 | [![Dynare 6.0 Docker](../../actions/workflows/docker-dynare-6.0.yml/badge.svg)](../../actions/workflows/docker-dynare-6.0.yml) |
|----------------|-----|

| Dynare 5 | [![Dynare 5.5 Docker](../../actions/workflows/docker-dynare-5.5.yml/badge.svg)](../../actions/workflows/docker-dynare-5.5.yml) | [![Dynare 5.4 Docker](../../actions/workflows/docker-dynare-5.4.yml/badge.svg)](../../actions/workflows/docker-dynare-5.4.yml) | [![Dynare 5.3 Docker](../../actions/workflows/docker-dynare-5.3.yml/badge.svg)](../../actions/workflows/docker-dynare-5.3.yml)
|----------------|-----|-----|-----|
|          | [![Dynare 5.2 Docker](../../actions/workflows/docker-dynare-5.2.yml/badge.svg)](../../actions/workflows/docker-dynare-5.2.yml) | [![Dynare 5.1 Docker](../../actions/workflows/docker-dynare-5.1.yml/badge.svg)](../../actions/workflows/docker-dynare-5.1.yml) | [![Dynare 5.0 Docker](../../actions/workflows/docker-dynare-5.0.yml/badge.svg)](../../actions/workflows/docker-dynare-5.0.yml) |

| Dynare 4 | [![Dynare 4.6.4 Docker](../../actions/workflows/docker-dynare-4.6.4.yml/badge.svg)](../../actions/workflows/docker-dynare-4.6.4.yml) |
|----------------|-------|


## Testing

Every Monday, the containers are tested using the [Dynare testsuite](https://git.dynare.org/Dynare/dynare/-/blob/master/tests). The tests are run on both MATLAB and Octave, and the results are published as GitHub Actions workflows.
The MATLAB workflows are expected to pass, whereas the ones for Octave may fail due to known issues with the testsuite and the base image the containers are built on.

Click on the badges for real-time status reports of the latest test runs.

| MATLAB | Octave |
|--------|--------|
| [![Testsuite 6.0 MATLAB](../../actions/workflows/testsuite-dynare-6.0-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-6.0-matlab.yml) | [![Testsuite Dynare 6.0 Octave](../../actions/workflows/testsuite-dynare-6.0-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-6.0-octave.yml) |
| [![Testsuite Dynare 5.5 MATLAB](../../actions/workflows/testsuite-dynare-5.5-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.5-matlab.yml) | [![Testsuite Dynare 5.5 Octave](../../actions/workflows/testsuite-dynare-5.5-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.5-octave.yml) |
| [![Testsuite Dynare 5.4 MATLAB](../../actions/workflows/testsuite-dynare-5.4-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.4-matlab.yml) | [![Testsuite Dynare 5.4 Octave](../../actions/workflows/testsuite-dynare-5.4-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.4-octave.yml) |
| [![Testsuite Dynare 5.3 MATLAB](../../actions/workflows/testsuite-dynare-5.3-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.3-matlab.yml) | [![Testsuite Dynare 5.3 Octave](../../actions/workflows/testsuite-dynare-5.3-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.3-octave.yml) |
| [![Testsuite Dynare 5.2 MATLAB](../../actions/workflows/testsuite-dynare-5.2-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.2-matlab.yml) | [![Testsuite Dynare 5.2 Octave](../../actions/workflows/testsuite-dynare-5.2-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.2-octave.yml) |
| [![Testsuite Dynare 5.1 MATLAB](../../actions/workflows/testsuite-dynare-5.1-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.1-matlab.yml) | [![Testsuite Dynare 5.1 Octave](../../actions/workflows/testsuite-dynare-5.1-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.1-octave.yml) |
| [![Testsuite Dynare 5.0 MATLAB](../../actions/workflows/testsuite-dynare-5.0-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.0-matlab.yml) | [![Testsuite Dynare 5.0 Octave](../../actions/workflows/testsuite-dynare-5.0-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-5.0-octave.yml) |
| [![Testsuite Dynare 4.6.4 MATLAB](../../actions/workflows/testsuite-dynare-4.6.4-matlab.yml/badge.svg)](../../actions/workflows/testsuite-dynare-4.6.4-matlab.yml) | [![Testsuite Dynare 4.6.4 Octave](../../actions/workflows/testsuite-dynare-4.6.4-octave.yml/badge.svg)](../../actions/workflows/testsuite-dynare-4.6.4-octave.yml) |

## Contributing

Contributions to improve the Docker containers or testing workflows are welcome. Please refer to the [contribution guidelines](https://git.dynare.org/Dynare/dynare/-/blob/master/CONTRIBUTING.md) for more information.

## Support

For questions or issues regarding Dynare or its Docker containers, please visit the [Dynare forums](https://forum.dynare.org).
