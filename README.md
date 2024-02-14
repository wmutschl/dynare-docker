# Dynare Docker Containers

[![Dynare 6.0](../../actions/workflows/dynare-6.0-matlab.yml/badge.svg)](../../actions/workflows/dynare-6.0-matlab.yml)
[![Dynare 5.5](../../actions/workflows/dynare-5.5-matlab.yml/badge.svg)](../../actions/workflows/dynare-5.5-matlab.yml)

This repository automates the testing of Dynare versions within Docker containers, ensuring reliability and stability across different environments.

## About Dynare

[Dynare](https://www.dynare.org) is a free software suite designed for analyzing and solving dynamic economic models. It can perform simulations, estimation, forecasting, and policy analysis.

## Docker Containers for Dynare

The Docker containers provide an isolated and consistent environment for running Dynare, facilitating easy deployment and testing across various systems. For more details on the containers, visit the [Dynare Docker Guide](https://git.dynare.org/Dynare/dynare/-/blob/master/scripts/docker/README.md).

## Testing Workflows

Currently, this repository contains only GitHub Actions workflows that trigger Dynare's test suite inside the Docker containers.

### Current Workflows

- **Dynare 6.0**: Automated tests for the Dynare 6.0 Docker container.
- **Dynare 5.5**: Automated tests for the Dynare 5.5 Docker container.

Click on the badges at the top for real-time status reports of the latest test runs. The MATLAB workflows are expected to pass, whereas the ones for Octave may fail due to known issues with the test suite and the base image the containers are built on.

## Contributing

Contributions to improve the testing workflows or to extend the support for more Dynare versions are welcome. Please refer to the [contribution guidelines](https://git.dynare.org/Dynare/dynare/-/blob/master/CONTRIBUTING.md) for more information.

## Support

For questions or issues regarding Dynare or its Docker containers, please visit the [Dynare forums](https://forum.dynare.org).
