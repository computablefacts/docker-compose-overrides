# Tests for docker compose overrides

With [Docker Compose](https://docs.docker.com/compose/), you can merge several
YAML files to get your configuration.

It can be used, for example, to add sppecific keys for development or to
change published port when deploying to production.

See the [official documentation](https://docs.docker.com/reference/compose-file/merge/)
for more details.


## Tests

To launch automated tests, you must first create a python virtual environment
with:

```bash
python3 -m venv .venv
```

Then, activate this virtual environment:

```bash
source .venv/bin/activate
```

And install dependencies:

```bash
pip install -r requirements.txt
```

Finally, you can now launch the tests:

```bash
pytest -v
```

When you're done, you can deactivate the virtual environment:

```bash
deactivate
```

## Add a new case

Each test case simulates a specific Docker Compose merge scenario. Follow these steps to add a new one.

PR are welcome!

### 1. Create a scenario folder

Create a new directory inside the `cases/` folder. The folder name should be descriptive of the test case (e.g., `15-ports-concat`, `17-volume-override`).

> [!NOTE]
> Folders starting with `_` (underscore) are ignored by the test runner.

### 2. Add Compose files

Inside your new folder, create your YAML files:

* `docker-compose.yaml` (Mandatory): This is the base configuration.
* `docker-compose.override.yaml`: The override file (you can name it differently, e.g., prod.yaml).

> [!NOTE]
> If you have multiple override files, they are applied in alphabetical order
> after the base file.

### 3. Generate the expected result (expected.yaml)

Instead of writing the expected result manually, you can generate it using Docker Compose.

Run the following commands in your terminal:

```bash
# 1. Navigate to your new case folder
cd cases/my_new_case

# 2. Generate the canonical config
docker compose -f docker-compose.yaml -f docker-compose.override.yaml config > expected.yaml
```

> [!IMPORTANT]
> Open `expected.yaml` and manually verify that the generated configuration
> matches what you actually expect. This file acts as the source of truth.

### 4. Run the Tests

Go back to the root of the repository and run the tests to ensure everything is
green:

```bash
pytest -v
```
