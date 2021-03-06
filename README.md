# python-patterns

This repo contains two projects as examples. 
The [first](./src/file_syncer) is meant to mimics an embedded system on a chip project.
The [second](./src/web_project) is meant to mimic a web-server based project. 

## Glossary of Terms

**Depenency** Generally used in two contexts. When getting a library from the internet (see poetry & pip) to use in your own application, it's generally referred to as installing and using a 'third party dependency'. That is, the application 'depends on' code from third party. The second context is within a single application, it refers to when one part of the software 'depends on' some other part of the software in order to function (see Dependency Injection). For example a Python class that handles http requests, may depend on a Python class that queries a database.

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

## [Domain Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design) 

An approach to writing software that emphasizes modeling business 'domains' and centralizing logic into domain 'models'. This discipline establishes lots of terms and can definitely be complicated. Like all design 'philosophies' it requires using good judgement as to how much or little it should or could be used. For the purposes of these examples the primary focosu is on centralizing business logic into core model classes that have no other dependencies. This approach makes greatly improves testing, discovering core business, and understanding the relationship of models which are very important things to get right in any large project. [Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.amazon.com/gp/product/0321125215/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) is a good *reference book* for terms and approaches, but is quite dry to attempt to work through entirely.

This is a common depiction of 'centering the domain model', where the core logic and code exists on a model, then things like 'services' or 'controllers' interact with the models , 'presenters' or 'views' transform those models into something for a user to see, and finally 'infrastructure' is how the application is deployed.

![domain driven design architecture](./docs/ddd.png)

### Model

A model should be a [simple class](https://pydantic-docs.helpmanual.io/usage/models/) that contains all of the properties and methods to interact with a 'domain model'. One way to think of how to create a good model, is to make sure the user of it knows what information they have access to, how it related to other models, and what are the safe ways to change the model.

A simple exmaple could be a `TodoModel` that related to a `UserModel`. A `todo` is created by a user, and can optionally be assigned to a user.

```python
class UserModel(BaseModel):
  id: int
  name: str

class TodoModel(BaseModel):
  id: int
  text: str
  created_by: UserModel
  assigned_to: Optional[UserModel]
```

The user that created the todo should never be changed after it's created, but the assignment can change whenever necessary. So the api for creating a `todo` should require the creating user and not be update-able.
There are also times when creating or updating a model requires a lot more validation of the relationship of models. 
In this contrived example we could consider users with the name "alec" to not allow to create tasks, and users with the name 
"scott" not allowed to be assigned tasks:

```python
class TodoModel(BaseModel):
  id: int = Field(allow_mutation=False)  # cannot change after creation
  text: str
  created_by: UserModel = Field(allow_mutation=False)  # cannot change after creation
  assigned_to: Optional[UserModel]

  @validate('created_by')
  def validate_created_by(cls, v: UserModel):
    if v.name == 'alec:
      raise ValueError('No way Alec.')
    return v

  @validate('assigned_to')
  def validate_created_by(cls, v: UserModel):
    if v.name == 'scott:
      raise ValueError('No way Scott.')
    return v

  class Config:
    validate_assignment = True  # validate on creation and when mutating fields

scott = UserModel(id = 1, name = "scott")
alec = UserModel(id = 2, name = "alec")
my_todo = TodoModel(id=1, created_by=scott, text="stuff")
my_todo.text "changed stuff"
my_todo.assigned_to = alec  # validator ran here
```

As relationships and logic gets more complicated update properties may need to be done via methods instead of direct 
assignment. For instance 


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



# TODO Nodes

- Order of the lesson?
  - folder structure
    - top level folder = project
      - utils top level shared code
    - main = production source code
    - test = test code / mocks
  - build & dependencies & tools
    - why poetry?
      - pip + requirements.txt + venv + build script + task runner + ...
    - how to use poetry
      - poetry shell
      - poetry add dependency
      - poetry add -D dependency
      - poetry install
      - poetry update
  
  - directory watcher
    - a process that watches a directory for changes
      - prints the changes to stdout with a logger
      - outputs metrics for changes
    - first implementation is 'bad'
    - second implementation:
      - externalize configuration (loop delay)
      - create the directory model
        - write models tests
      - split out the directory api
        - write api tests
      - update worker tests to use a mock api for simplicity
      - can now create a cli
      - logging & metrics is vastly improved
        - statsd: nc -lu 8125
        - json logs: nc -l 5170 
    - add another worker that listens to events and synchronizes files
      - on each file change event reflects the change in another directory
      - write worker_utils BaseWorker
      - shares a message queue with the other worker
        - is the message queue some api or just share the queue directly?
      - main.py has to launch two workers now
     
  - directory sync web service
    - http POST directory changes
      - writes all changes to local directory
    - web page to view the directory and its contents
    - http client implementation that implements the same interface as the ctrl
    - cli to web server to simulate events
    - update directory watcher to no longer depend on a queue, but an api
      - one api is a local in process queue and worker
      - other api is an http client to the web server
      - configuration for embedded project to sync local vs remote
    - tests
      - ctrl
      - functional (whole web server) that uses the http client
