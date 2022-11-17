# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0.dev1] - 2022-11-17

### Added

- test examples, including app and tasks.
- changelog description.
- codecov action.

### Changed

- fix ContextVar not propagated from fixture to test.
- change `starlette = ">=0.20.14"` to `starlette = ">=0.19.1"`.

### Removed

- test_database.py and test_middleware.py

### Others

- modify use case in README.md
- add changelog description.
- update codecov action.
- modify test case.

## [0.0.1.dev0] - 2022-11-09

### Added

- sqlalchemy ctx use ContextVar
- fastapi middleware use sqlalchemy ctx