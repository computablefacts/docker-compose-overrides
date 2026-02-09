#!/usr/bin/env python3
from pathlib import Path

CASES_DIR = Path(__file__).parent / "cases"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").rstrip()


def generate_readme(case_dir: Path):
    case_name = case_dir.name

    yaml_files = sorted(
        f for f in case_dir.glob("*.yaml")
        if f.name != "expected.yaml"
    )

    if not (case_dir / "expected.yaml").exists():
        print(f"Skipping {case_name}: no expected.yaml")
        return

    if not any(f.name == "docker-compose.yaml" for f in yaml_files):
        print(f"Skipping {case_name}: no docker-compose.yaml")
        return

    # Ensure base file is first
    yaml_files = (
        [case_dir / "docker-compose.yaml"]
        + [f for f in yaml_files if f.name != "docker-compose.yaml"]
    )

    expected_file = case_dir / "expected.yaml"

    lines = []
    lines.append(f"# Case: {case_name}\n")
    lines.append("## Description\n")
    lines.append(
        "This case documents how Docker Compose merges configuration files "
        "when multiple compose files are used.\n"
    )
    lines.append("---\n")

    # Base + overrides
    lines.append("## Input configurations\n")

    for yaml_file in yaml_files:
        lines.append(f"### {yaml_file.name}\n")
        lines.append("```yaml")
        lines.append(read_file(yaml_file))
        lines.append("```\n")

    lines.append("---\n")

    # Expected
    lines.append("## Expected merged configuration\n")
    lines.append("### expected.yaml\n")
    lines.append("```yaml")
    lines.append(read_file(expected_file))
    lines.append("```\n")

    lines.append("---\n")

    # Command
    lines.append("## Command used\n")
    lines.append("```bash")
    lines.append("docker compose \\")
    for f in yaml_files:
        lines.append(f"  -f {f.name} \\")
    lines.append("  config")
    lines.append("```\n")

    readme_path = case_dir / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {readme_path}")


def main():
    if not CASES_DIR.exists():
        raise RuntimeError(f"Cases directory not found: {CASES_DIR}")

    for case_dir in sorted(d for d in CASES_DIR.iterdir() if d.is_dir()):
        generate_readme(case_dir)


if __name__ == "__main__":
    main()
