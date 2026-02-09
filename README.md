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
