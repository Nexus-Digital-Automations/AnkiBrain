VERSION = "0.7.4"

import os
import sys
import time
from os import path

# Initialize performance logging as early as possible
startup_timer = time.time()

# Necessary to bootstrap this way so we can start importing other modules in the root folder.
sys.path.insert(1, path.abspath(path.dirname(__file__)))

# Import performance logging system
from performance_logger import (
    get_performance_logger,
    log_startup_phase,
    PerformanceTimer,
)

# Create logger for main initialization
logger = get_performance_logger("AnkiBrainInit")
logger.startup_info(
    f"AnkiBrain v{VERSION} initialization started", {"version": VERSION}
)

with PerformanceTimer(logger, "import_project_paths"):
    from project_paths import (
        ChatAI_module_dir,
        version_file_path,
        venv_site_packages_path,
        bundled_deps_dor,
    )

with PerformanceTimer(logger, "setup_python_paths"):
    logger.startup_info(
        "Setting up Python module paths",
        {
            "ChatAI_module_dir": ChatAI_module_dir,
            "venv_site_packages_path": venv_site_packages_path,
            "bundled_deps_dor": bundled_deps_dor,
        },
    )
    sys.path.insert(1, ChatAI_module_dir)
    sys.path.insert(1, venv_site_packages_path)

    # Also insert bundled_dependencies folder for server mode (needs httpx lib).
    sys.path.insert(1, bundled_deps_dor)

with PerformanceTimer(logger, "import_anki_dependencies"):
    from anki.hooks import addHook
    from aqt import mw
    from aqt.qt import *

with PerformanceTimer(logger, "setup_version_file"):
    mw.CURRENT_VERSION = VERSION
    if path.isfile(version_file_path):
        logger.startup_info(
            "Removing existing version file", {"path": version_file_path}
        )
        os.remove(version_file_path)
    with open(version_file_path, "w") as f:
        f.write(mw.CURRENT_VERSION)
    logger.startup_info(
        "Created version file", {"version": VERSION, "path": version_file_path}
    )

with PerformanceTimer(logger, "import_boot_modules"):
    from boot import load_ankibrain, add_ankibrain_menu

log_startup_phase(
    "Module imports completed",
    {"total_init_time_ms": round((time.time() - startup_timer) * 1000, 2)},
)


def handle_anki_boot():
    """
    Main Anki boot handler - executed when Anki profile is loaded.
    This is where the actual AnkiBrain initialization begins.
    """
    boot_logger = get_performance_logger("AnkiBootHandler")
    boot_logger.startup_info("Anki profile loaded - starting AnkiBrain boot sequence")

    with PerformanceTimer(boot_logger, "add_ankibrain_menu"):
        # This function body gets executed once per boot, so we ensure we don't add duplicate menu buttons.
        add_ankibrain_menu()

    with PerformanceTimer(boot_logger, "setup_menu_actions"):
        # Keep track of menu actions references, so we can delete them later if we need to.
        mw.menu_actions = []

    with PerformanceTimer(boot_logger, "load_ankibrain_main"):
        # Ignition sequence - this is where the heavy lifting happens
        boot_logger.startup_info("Starting main AnkiBrain loading sequence")
        load_ankibrain()

    boot_logger.startup_info("AnkiBrain boot sequence completed successfully")
    log_startup_phase("AnkiBrain fully initialized")


logger.startup_info("Registering profileLoaded hook")
addHook("profileLoaded", handle_anki_boot)
