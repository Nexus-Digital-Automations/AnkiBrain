#!/usr/bin/env python3
"""
AnkiBrain Development Environment Setup Script for macOS

This script sets up the complete development environment for AnkiBrain,
including virtual environment validation, dependency verification, and
environment configuration for development and testing.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def print_status(message, success=None):
    """Print colored status messages"""
    if success is True:
        print(f"✅ {message}")
    elif success is False:
        print(f"❌ {message}")
    else:
        print(f"🔄 {message}")


def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_status(f"{description} - Success", True)
            return True, result.stdout
        else:
            print_status(f"{description} - Failed: {result.stderr}", False)
            return False, result.stderr
    except Exception as e:
        print_status(f"{description} - Error: {str(e)}", False)
        return False, str(e)


def check_python_version():
    """Check Python version compatibility"""
    print_status("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print_status(
            f"Python {version.major}.{version.minor}.{version.micro} is compatible",
            True,
        )
        return True
    else:
        print_status(
            f"Python {version.major}.{version.minor}.{version.micro} is too old (need 3.9+)",
            False,
        )
        return False


def check_virtual_environment():
    """Check and validate virtual environment"""
    print_status("Checking virtual environment setup...")

    venv_path = Path("user_files/venv")
    if not venv_path.exists():
        print_status("Virtual environment not found, creating...", None)
        success, output = run_command(
            "python3 -m venv user_files/venv", "Creating virtual environment"
        )
        if not success:
            return False

    # Check if venv has required structure
    required_paths = [
        venv_path / "bin" / "python",
        venv_path / "bin" / "pip",
        venv_path / "bin" / "activate",
    ]

    for path in required_paths:
        if not path.exists():
            print_status(f"Missing required file: {path}", False)
            return False

    print_status("Virtual environment structure validated", True)
    return True


def check_dependencies():
    """Check if all required dependencies are installed"""
    print_status("Checking installed dependencies...")

    venv_python = "user_files/venv/bin/python"
    venv_pip = "user_files/venv/bin/pip"

    # Upgrade pip first
    success, _ = run_command(f"{venv_pip} install --upgrade pip", "Upgrading pip")
    if not success:
        return False

    # Check if requirements are installed
    success, output = run_command(
        f"{venv_pip} list --format=freeze", "Getting installed packages"
    )
    if not success:
        return False

    installed_packages = {
        line.split("==")[0].lower()
        for line in output.strip().split("\n")
        if "==" in line
    }

    # Check critical packages
    critical_packages = ["anki", "aqt", "openai", "langchain", "pyqt6"]
    missing_packages = []

    for package in critical_packages:
        if package.lower() not in installed_packages:
            missing_packages.append(package)

    if missing_packages:
        print_status(f"Missing critical packages: {', '.join(missing_packages)}", False)
        print_status("Installing from requirements.txt...", None)
        success, _ = run_command(
            f"{venv_pip} install -r requirements.txt", "Installing requirements"
        )
        return success
    else:
        print_status(
            f"All critical packages installed: {', '.join(critical_packages)}", True
        )
        return True


def create_development_config():
    """Create development configuration files"""
    print_status("Creating development configuration...")

    # Create a development settings file
    dev_config = {
        "environment": "development",
        "debug_mode": True,
        "log_level": "DEBUG",
        "virtual_environment": str(Path("user_files/venv").absolute()),
        "python_executable": str(Path("user_files/venv/bin/python").absolute()),
        "requirements_file": "requirements.txt",
        "setup_date": "2025-09-13",
        "platform": "macOS",
        "notes": [
            "Virtual environment configured for macOS development",
            "All dependencies installed and validated",
            "Ready for AnkiBrain development and testing",
        ],
    }

    config_path = Path("development_config.json")
    try:
        with open(config_path, "w") as f:
            json.dump(dev_config, f, indent=2)
        print_status(f"Development config created: {config_path}", True)
        return True
    except Exception as e:
        print_status(f"Failed to create config: {str(e)}", False)
        return False


def test_basic_imports():
    """Test basic module imports"""
    print_status("Testing basic imports...")

    venv_python = "user_files/venv/bin/python"

    test_imports = [
        ("anki", "Core Anki library"),
        ("aqt", "Anki Qt interface"),
        ("openai", "OpenAI API client"),
        ("langchain", "LangChain framework"),
        ("PyQt6.QtCore", "PyQt6 core"),
    ]

    success_count = 0
    for module, description in test_imports:
        cmd = f"{venv_python} -c 'import {module}; print(\"✅ {description}\")'"
        success, output = run_command(cmd, f"Testing {description}")
        if success:
            success_count += 1

    if success_count == len(test_imports):
        print_status("All basic imports successful", True)
        return True
    else:
        print_status(
            f"Only {success_count}/{len(test_imports)} imports successful", False
        )
        return False


def create_activation_script():
    """Create a convenient activation script for development"""
    print_status("Creating development activation script...")

    script_content = """#!/bin/bash
# AnkiBrain Development Environment Activation Script
# Generated on 2025-09-13

echo "🚀 Activating AnkiBrain Development Environment..."

# Activate virtual environment
source user_files/venv/bin/activate

# Set environment variables
export ANKIBRAIN_DEV=1
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify activation
echo "✅ Virtual environment activated"
echo "📍 Python: $(which python)"
echo "📦 Pip: $(which pip)"
echo "🏠 Project root: $(pwd)"
echo ""
echo "🧠 AnkiBrain development environment ready!"
echo ""
echo "To run development commands:"
echo "  python -m ruff check .                    # Run linting"
echo "  python -c 'from performance_logger import get_performance_logger; print(\"Logger works!\")'"
echo ""
echo "To deactivate: deactivate"
"""

    script_path = Path("activate_dev.sh")
    try:
        with open(script_path, "w") as f:
            f.write(script_content)

        # Make script executable
        os.chmod(script_path, 0o755)

        print_status(f"Development activation script created: {script_path}", True)
        print_status("Usage: source ./activate_dev.sh", None)
        return True
    except Exception as e:
        print_status(f"Failed to create activation script: {str(e)}", False)
        return False


def main():
    """Main setup function"""
    print("🧠 AnkiBrain Development Environment Setup")
    print("=" * 50)

    # Checklist of setup tasks
    tasks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies", check_dependencies),
        ("Development Config", create_development_config),
        ("Basic Imports", test_basic_imports),
        ("Activation Script", create_activation_script),
    ]

    success_count = 0
    for task_name, task_func in tasks:
        print(f"\n📋 {task_name}:")
        if task_func():
            success_count += 1
        else:
            print_status(f"Task failed: {task_name}", False)

    print("\n" + "=" * 50)
    print(f"📊 Setup Results: {success_count}/{len(tasks)} tasks completed")

    if success_count == len(tasks):
        print_status("🎉 AnkiBrain development environment setup complete!", True)
        print("\n📋 Next steps:")
        print("1. source ./activate_dev.sh")
        print("2. python -m ruff check .")
        print("3. Start developing!")
        return True
    else:
        print_status("⚠️ Setup completed with some issues", False)
        print("\n📋 Review failed tasks above and resolve issues")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
