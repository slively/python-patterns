# python-patterns

This repo contains two projects as examples. 
The [first](./src/embedded_project) is meant to mimics an embedded system on a chip project.
The [second][./src/web_project] is meant to mimic a web-server based project. 

## Glossary of Terms

**Depenency** Generally used in two contexts. When getting a library from the internet (see poetry & pip) to use in your own application, it's generally referred to as installing and using a 'third party dependency'. That is, the application 'depends on' code from third party. The second context is within a single application, it refers to when one part of the software 'depends on' some other part of the software in order to function (see Dependency Injection). For example a Python class that handls http requests, may depend on a Python class that queries a database.

**Dependency Injection** A [very common](https://en.wikipedia.org/wiki/Dependency_injection) software engineering pattern meant to reduce [coupling](https://en.wikipedia.org/wiki/Coupling_(computer_programming) of software components. Also see 'Externalized Configuration'.

For example, a Python class that uses a database client will receive a client as a constructor argument as opposed to constructing the client internally in the class. This makes it much easier to replace the database client implementation. This is especially useful in writing software that is 'testable'.

This would be considered code that is 'tightly coupled' and not using dependency injection:
```python
class MyClass:

    def query_database(self):
        db_client = SomeDbClient("http://localhost")
        return db_client.select_all()
```

This would be consideered 'loosely coupled' and using dependency injection:
```python
class MyClass:

    def __init(self, db_client: SomeDbClient):
        self.db_client = db_client

    def query_database(self):
        return self.db_client.select_all()
```

**Externalized Configuration** A very common software engineering pattern where any configuration for the software can be done without changing the source code, but instead by changing some external value. A very common pattern would be to use environment variables, and a common python library for doing this is `argparse`. Very important for things like urls to databases or external services, file paths where the software may read/write files, and constant values that could determine timeouts or retry logic.

**Test** A test is simply software used to test other software. In Python a common library for achieving this is `unittest`.

**Test Mock** A test mock is an implementation of an api where the behavior of the api is mimic'd for a test. For example a mock for a file api could be setup to return a hard coded set of files to setup a very specific test case.

**Unit Test** A unit test is mean to test a single 'unit' of code that tends to represent a single piece of business logic. A common unit test would test a single method on a class that implements some larger api. It's also very common to 'mock' any dependencies of the class being tested to focus on testing just the single unit of business logic and not the dependencies. This tends to be the most common type of test in a project.

**Integration Test** An integration test is very similar to a unit test, but would opt to use more real dependencies instead of using mocks. It may still use mocks as an integration test may not run th entire software stack. If a unit test is to test one thing, then an integration is to test that multiple apis and dependencies interact together correctly. This tends to be a test written when components have a complex interaction and it's important that they are setup correctly. For example two workers that coordinate work via a message queue.

**Functional Test** A functional test should test the entire software stack as close to production as possible. Ideally it would involve running an entire web-server, worker, cli, web page, etc... and asserting the software works from the perspective of a user. These tests tend to be written to mimic actual behavior of users. For web pages it may even automate running a browser and simulating clicks. These tests take the longest to write, take the longest to run, and are the hardest to maintain, BUT if a project has a good system for writing and running these tests, they tend to be the most valuable. Nothing will help you sleep at night better than knowing you have an automated system that actually runs the entire software stack and behaves as a user everytime you make a change.

**Database ORM** A [very common](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) software engineering pattern for converting data from a database data into in memory representations. For example, `sqlalchemy` is a Python library that can query a SQL database and turn the results into a Python class. Some ORMs have a whole lot of features, some try to be as small as possible and there's lots of debate as to which is better. One of the most important features is protecting against [injection attacks](https://en.wikipedia.org/wiki/SQL_injection).

**Linter** A program that analysizes source code (in this case Python source code) verifying the code was written with a specific 'style' (see PEP8 & flake8).

**PEP8** The Python community standard [style guide](https://peps.python.org/pep-0008/) for Pythong source code.

**flake8** A linter for Python that verifies source code adheres to the PEP8 standard.

**Static Type Checker** Python in particular is an [interpreted](https://en.wikipedia.org/wiki/Interpreter_(computing) language as opposed to a [compiled](https://en.wikipedia.org/wiki/Compiler) language. Python is also [dynamically typed](https://en.wikipedia.org/wiki/Dynamic_programming_language) vs [statically typed](https://en.wikipedia.org/wiki/Type_system#Static_type_checking), but there is now a package in the Python called `typings` that allows for [type annotations](https://en.wikipedia.org/wiki/Type_signature). __A static type checker is a program that can be run against source code that will check the type annotations in the code to ensure they are correct.__ When running a Python program, these type annotations are completely ignored by the interpreter just like comments. Lots of other languages like Java and C++ have the static type checker built into the compiler. Another similar Python typings is [Typescript](https://www.typescriptlang.org/) which is Javascript + type annotations. It has a compiler that does all static type checking, then removes all type annotations, and finally writes standard javascript files.

## Structure

This is setup as a kind of multi-project monorepo. The biggest downside is all projects share the same set of poetry dependencies. It does allow all code to share a single [utils](./src/utils) project. All code is in [src](./src) and each project is a top level directory in src. Within each project there is a `main` directory for production code, and a `tests` directory for all tests.

## Build / Dependencies

The following development tools are used:
  - Dependencies: poetry
    - see [pyproject.toml](./pyproject.toml)
  - Linting: flake8
    - see [.flake8](./.flake8)
  - Formatting: black
    - vscode has a plugin to autoformat files
  - Type Checking: mypy
    - see [pyproject.toml](./pyproject.toml)
  - Tests: unittest
    
Poetry is configured with commands that use [build.py](./src/build.py) for convenience:
```
poetry run lint
poetry run typecheck
poetry run test

# run all of the above
poetry run build
```


## Example Embedded Project

This project just has a simple worker implementation that monitors a directory for changes. There is also a cli for interesting with the directory api manually.

Running the worker can be run with poetry (this will monitor the .vscode directory):
```shell
poetry run worker --dir ./.vscode
```

Running the cli can be run with poetry:
```shell
poetry run cli list --dir ./.vscode
poetry run cli reset --dir ./tmp
```

## Example Web Server Project

This project implements a simple todos web api with a simple html form based gui. There is also a cli that interacts with the web server. 

The tech stack of the web project is:
    - database: sqlite (defaults to in memory database)
    - database orm: sqlalchemy
    - web server: fastapi
    - html templates: jinja2
    - http client: requests

The datastore is sqlite using `:memory:` mode by default.
