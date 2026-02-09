import pytest
import subprocess
import yaml
import os
from pathlib import Path
from deepdiff import DeepDiff

# Path to the directory containing test cases
CASES_DIR = Path(__file__).parent.parent / "cases"

def get_scenarios():
    """
    Scan the cases/ directory to find all scenario subdirectories.
    Returns a list of directory names.
    """

    print(CASES_DIR)

    if not CASES_DIR.exists():
        return []

    return [
        d.name for d in CASES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith('_')  # Ignore directories starting with _
    ]

def normalize_paths(yaml_content, root_path):
    """
    Docker Compose config generates absolute paths.
    This function replaces the absolute path of the test case directory
    with '.' to make the comparison portable across environments.
    """
    return yaml_content.replace(str(root_path.resolve()), ".")

@pytest.mark.parametrize("scenario_name", get_scenarios())
def test_docker_compose_override(scenario_name):
    """
    Parameterized test: runs once for each scenario directory.
    """
    scenario_path = CASES_DIR / scenario_name

    # 1. Identify compose files to merge
    # We take all .yaml files except expected.yaml
    # We sort them to ensure deterministic order:
    # docker-compose.yaml first, then override files
    files = sorted([
        f.name for f in scenario_path.glob("*.yaml")
        if f.name != "expected.yaml"
    ])

    # Basic validation
    if "docker-compose.yaml" not in files:
        pytest.fail(f"Scenario {scenario_name} does not contain docker-compose.yaml")

    # Ensure docker-compose.yaml is first (base), followed by overrides
    files.remove("docker-compose.yaml")
    files.insert(0, "docker-compose.yaml")

    # 2. Build the docker compose config command
    cmd = ["docker", "compose"]
    for f in files:
        cmd.extend(["-f", str(scenario_path / f)])
    cmd.append("config")

    # 3. Run the command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        pytest.fail(
            f"Error while generating the compose configuration:\n{result.stderr}"
        )

    # 4. Normalize and parse the generated YAML
    # Replace absolute paths with '.' to match expected.yaml
    normalized_output = normalize_paths(result.stdout, scenario_path)
    generated_config = yaml.safe_load(normalized_output)

    # 5. Load the expected result
    expected_file = scenario_path / "expected.yaml"
    if not expected_file.exists():
        pytest.fail(f"No expected.yaml file found for scenario {scenario_name}")

    with open(expected_file, 'r') as f:
        expected_config = yaml.safe_load(f)

    # 6. Smart structural comparison
    # ignore_order=True is important for lists where order does not matter
    # (e.g. environment variables in some cases).
    # Be careful: for keys like 'ports' or 'command', order may matter.
    # DeepDiff is configurable; here we compare strictly while ignoring ordering.
    diff = DeepDiff(
        expected_config,
        generated_config,
        ignore_order=True,
        report_repetition=True
    )

    # If diff is not empty, the test fails with a clear message
    assert not diff, (
        f"Generated configuration does not match expected output "
        f"for scenario {scenario_name}.\nDifferences:\n{diff.pretty()}"
    )
