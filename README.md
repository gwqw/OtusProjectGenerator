# OtusProjectGenerator
Generator initial project structure for otus-cpp homewrk. It will create initial project file structure for fast development start.

## Description

edit  parameters in `proj_gen.cfg`:

- `PATH` -- where to create project
- `PROJECT_NAME`-- project name: it will be project name in cmake, exe-name and bin package name
- `SOURCE_LIST` -- sources (cpp and header) they will be included in exe and test
- `TEST_SOURCE_LIST` -- sources for BOOST test framework, empty -- no tests (and no boost dependency)

## Run

```sh
./otus_project_generator.py
```

