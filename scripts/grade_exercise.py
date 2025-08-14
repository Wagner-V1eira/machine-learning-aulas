#!/usr/bin/env python3
"""Grade exercise script."""

import argparse
import json
import sys
from pathlib import Path

# Setup path before imports
sys.path.insert(0, str(Path(__file__).parent.parent))  # noqa: E402

from core.grading.api import grade_exercise  # noqa: E402


def main() -> None:
    """Main grading function."""
    parser = argparse.ArgumentParser(description="Grade student exercise")
    parser.add_argument("notebook", help="Path to student notebook")
    parser.add_argument("tests", help="Path to test file")
    parser.add_argument(
        "--allowed-imports",
        nargs="*",
        default=["numpy", "pandas", "sklearn", "matplotlib", "scipy"],
        help="Allowed import modules",
    )
    parser.add_argument("--output", "-o", help="Output file for results")

    args = parser.parse_args()

    # Validate files exist
    notebook_path = Path(args.notebook)
    tests_path = Path(args.tests)

    if not notebook_path.exists():
        print(f"Error: Notebook not found: {notebook_path}")
        sys.exit(1)

    if not tests_path.exists():
        print(f"Error: Tests not found: {tests_path}")
        sys.exit(1)

    # Grade exercise
    print(f"Grading exercise: {notebook_path.name}")
    print(f"Using tests: {tests_path.name}")

    allowed_imports = set(args.allowed_imports)
    result = grade_exercise(str(notebook_path), str(tests_path), allowed_imports)

    # Display results
    print(f"\n{'='*50}")
    print("RESULTS")
    print(f"{'='*50}")
    print(f"Score: {result['score']}/100")
    print(f"Passed: {result['passed_tests']}/{result['total_tests']} tests")
    print(f"Status: {result['status']}")

    if result["status"] == "error":
        print(f"Error: {result['error']}")

    # Show test details
    if result["test_results"]:
        print("\nTest Details:")
        for test in result["test_results"]:
            status = "✓" if test["passed"] else "✗"
            print(f"  {status} {test['name']}")
            if test["error"]:
                print(f"    Error: {test['error']}")

    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")

    # Exit with error code if grading failed
    if result["status"] == "error" or result["score"] == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
