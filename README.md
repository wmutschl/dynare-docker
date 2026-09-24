# Dynare Docker Containers
[Dynare](https://www.dynare.org) is a free software suite designed for analyzing and solving dynamic economic models. It can perform simulations, estimation, forecasting, and policy analysis.
The Dynare team provides Docker containers for running Dynare on both MATLAB and Octave and publishes them on [Docker Hub](https://hub.docker.com/r/dynare/dynare). For details on how to use the containers, see the [Dynare Docker Guide](docker/README.md).

This repository contains the [Dockerfile](docker/Dockerfile) and automates building, pushing and testing the containers with GitHub Actions.

| Workflow | Status | What it does |
|----------|--------|--------------|
| [Build Docker images](.github/workflows/build.yml) | [![Build Docker images](../../actions/workflows/build.yml/badge.svg)](../../actions/workflows/build.yml) | Builds all monthly images on the 21st of each month and pushes them to Docker Hub |
| [Dynare testsuite](.github/workflows/testsuite.yml) | [![Dynare testsuite](../../actions/workflows/testsuite.yml/badge.svg)](../../actions/workflows/testsuite.yml) | Runs the Dynare testsuite with Octave and MATLAB every Monday |
| [Keep scheduled workflows alive](.github/workflows/keepalive.yml) | [![Keepalive](../../actions/workflows/keepalive.yml/badge.svg)](../../actions/workflows/keepalive.yml) | Prevents GitHub from disabling the scheduled workflows after 60 days of inactivity |

The status of each individual image is shown per matrix job on the workflow run pages.

## Versions

[versions.json](versions.json) is the single source of truth for the images:

| Dynare | MATLAB | Octave | Ubuntu | Rebuilt |
|--------|--------|--------|--------|---------|
| 7.2 (`latest`) | R2026a | 8.4.0 | 24.04 | monthly |
| 7.1 | R2026a | 8.4.0 | 24.04 | monthly |
| 7.0 | R2025b | 8.4.0 | 24.04 | monthly |
| 6.5 | R2025b | 8.4.0 | 24.04 | monthly |
| 6.4 | R2025a | 8.4.0 | 24.04 | monthly |
| 6.3 | R2024b | 8.4.0 | 24.04 | monthly |
| 6.2 | R2024b | 8.4.0 | 24.04 | monthly |
| 6.1 | R2024a | 8.4.0 | 24.04 | monthly |
| 6.0 | R2023b | 8.4.0 | 24.04 | monthly |
| 5.5, 5.4 | R2023b, R2023a | 8.4.0 | 24.04 | manual |
| 5.3 – 5.0, 4.6.4 | R2022b – R2021a | 5.2.0 | 20.04 | manual |

For each Dynare release we use the newest MATLAB release it supports. Every image is tagged `X.Y`, `X.Y-<MATLAB release>` and `X.Y-<MATLAB release>-<date>`; `latest` points to the newest Dynare release.

### Adding a new Dynare release

1. Add a line to [versions.json](versions.json) (move `"latest": true` to the new entry if applicable) and update the tag tables in this README and in [docker/README.md](docker/README.md).
2. Run the [build workflow](../../actions/workflows/build.yml) manually with the new version (e.g. `7.3`), then the [testsuite workflow](../../actions/workflows/testsuite.yml) for the same version.

Other combinations can be built on demand by dispatching the build workflow with e.g. `6.1-R2023b`; such images are only tagged `X.Y-<MATLAB release>` and `X.Y-<MATLAB release>-<date>`.

## Docker builds

The build workflow builds the images from [docker/Dockerfile](docker/Dockerfile) on GitHub-hosted runners (building needs no MATLAB license) and pushes them to Docker Hub using the `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD` secrets.
Every build ends with a quick Dynare run under Octave as a smoke test.
Pull requests and pushes to other branches that touch the Dockerfile build the `latest` image without pushing it.

## Testing

The testsuite workflow runs the [Dynare testsuite](https://git.dynare.org/Dynare/dynare/-/tree/master/tests) inside the published images:

- **Octave** tests run on GitHub-hosted runners.
- **MATLAB** tests run on a self-hosted runner with access to a MATLAB license (see below). If the runner is offline, the MATLAB jobs wait in the queue until it comes back (or until they time out).

Known failing tests can be skipped per version and testsuite with `test_excludes` in [versions.json](versions.json). Test logs are uploaded as workflow artifacts.

### Self-hosted runner for MATLAB

1. On a Linux machine with Docker and network access to your MATLAB license server, [add a self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners) to this repository and give it the additional label `matlab` (the jobs use `runs-on: [self-hosted, linux, matlab]`). Make sure the runner user can run `docker` and that there is enough disk space for the images (~20 GB each; clean up old ones with `docker image prune`).
2. Add a repository secret `MLM_LICENSE_FILE` containing the license server, e.g. `27000@matlab-campus.uni-tuebingen.de`. It is passed to the containers as the `MLM_LICENSE_FILE` environment variable.
3. Run the testsuite workflow manually with `suites: matlab` to check the setup.

For security reasons, do not use the self-hosted runner for workflows triggered by pull requests from forks (the testsuite workflow only runs on schedule and on manual dispatch).

## Contributing

Contributions to improve the Docker containers or testing workflows are welcome. Please refer to the [contribution guidelines](https://git.dynare.org/Dynare/dynare/-/blob/master/CONTRIBUTING.md) for more information.

## Support

For questions or issues regarding Dynare or its Docker containers, please visit the [Dynare forums](https://forum.dynare.org).
