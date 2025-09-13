import shutil
from os import path

from aqt import mw
from aqt.utils import showInfo

from project_paths import root_project_dir
from performance_logger import (
    get_performance_logger,
    PerformanceTimer,
    log_startup_phase,
)

# Create logger for boot operations
boot_logger = get_performance_logger("BootModule")
boot_logger.startup_info("Boot module loaded")


def add_ankibrain_menu():
    """Create AnkiBrain menu in Anki's menu bar."""
    with PerformanceTimer(boot_logger, "create_ankibrain_menu"):
        boot_logger.startup_info("Creating AnkiBrain menu")
        ankibrain_menu = mw.form.menubar.addMenu("AnkiBrain")
        mw.ankibrain_menu = ankibrain_menu
        boot_logger.startup_info("AnkiBrain menu created successfully")


def run_boot_checks():
    """
    Check for python dependencies in user_files/venv
    TODO: check if installed dependencies match requirements.txt
    :return:
    """
    with PerformanceTimer(boot_logger, "run_boot_checks"):
        boot_logger.startup_info("Running boot checks")

        # Delete /venv, it should be in /user_files/venv. This should work since the ChatAI module
        # has not powered on, so venv is not being used.
        old_venv_path = path.join(root_project_dir, "venv")

        if path.isdir(old_venv_path):
            boot_logger.startup_warning(
                "Found old venv directory - removing", {"path": old_venv_path}
            )
            try:
                shutil.rmtree(old_venv_path)
                boot_logger.startup_info("Successfully removed old venv directory")
            except Exception as e:
                boot_logger.startup_error(
                    "Failed to remove old venv directory",
                    {"error": str(e)},
                    exc_info=True,
                )
                print(str(e))
        else:
            boot_logger.startup_info("No old venv directory found - clean state")

        boot_logger.startup_info("Boot checks completed")


def load_ankibrain():
    """Main AnkiBrain loading function - determines and loads appropriate mode."""
    print("Booting AnkiBrain...")
    boot_logger.startup_info("Starting AnkiBrain load sequence")
    log_startup_phase("Beginning AnkiBrain load")

    with PerformanceTimer(boot_logger, "boot_checks"):
        run_boot_checks()

    with PerformanceTimer(boot_logger, "import_core_modules"):
        boot_logger.startup_info("Importing core modules")
        from util import UserMode
        from settings import SettingsManager
        from project_paths import settings_path

    with PerformanceTimer(boot_logger, "initialize_settings_manager"):
        boot_logger.startup_info(
            "Initializing settings manager", {"settings_path": settings_path}
        )
        mw.settingsManager = SettingsManager(pth=settings_path)
        user_mode: UserMode = mw.settingsManager.get_user_mode()
        boot_logger.startup_info(
            "User mode determined", {"mode": user_mode.name if user_mode else "None"}
        )

    if user_mode == UserMode.LOCAL:
        boot_logger.startup_info("Loading AnkiBrain in LOCAL mode")
        load_ankibrain_local_mode()
    elif user_mode == UserMode.SERVER:
        boot_logger.startup_info("Loading AnkiBrain in SERVER mode")
        load_ankibrain_server_mode()
    else:
        boot_logger.startup_warning("No user mode set - showing mode selection dialog")
        # No mode set, ask the user.
        with PerformanceTimer(boot_logger, "import_user_mode_dialog"):
            from UserModeDialog import show_user_mode_dialog

        show_user_mode_dialog()

    boot_logger.startup_info("AnkiBrain load sequence completed")
    log_startup_phase("AnkiBrain load completed")


def load_ankibrain_local_mode():
    """Load AnkiBrain in local mode - handles installation check and AnkiBrain instance creation."""
    print("Loading AnkiBrain in Local Mode...")
    boot_logger.startup_info("Entering local mode loading sequence")
    log_startup_phase("Loading AnkiBrain Local Mode")

    with PerformanceTimer(boot_logger, "import_local_mode_dependencies"):
        from util import has_ankibrain_completed_install, UserMode
        from InstallDialog import InstallDialog, show_install_dialog

    with PerformanceTimer(boot_logger, "check_installation_status"):
        installation_complete = has_ankibrain_completed_install()
        boot_logger.startup_info(
            "Installation status checked", {"installed": installation_complete}
        )

    if installation_complete:
        boot_logger.startup_info(
            "AnkiBrain installation detected - creating main instance"
        )

        with PerformanceTimer(boot_logger, "import_ankibrain_module"):
            from AnkiBrainModule import AnkiBrain

        with PerformanceTimer(boot_logger, "create_ankibrain_instance"):
            boot_logger.startup_info("Creating AnkiBrain instance in LOCAL mode")
            ankiBrain = AnkiBrain(user_mode=UserMode.LOCAL)
            mw.ankiBrain = ankiBrain
            boot_logger.startup_info(
                "AnkiBrain instance created and assigned to mw.ankiBrain"
            )
    else:
        boot_logger.startup_warning(
            "AnkiBrain not fully installed - showing installation dialog"
        )

        with PerformanceTimer(boot_logger, "setup_installation_dialog"):
            mw.installDialog = InstallDialog(mw)
            mw.installDialog.hide()
            boot_logger.startup_info("Installation dialog created")

        with PerformanceTimer(boot_logger, "setup_installation_menu"):
            from AnkiBrainModule import add_ankibrain_menu_item

            add_ankibrain_menu_item("Install...", show_install_dialog)
            boot_logger.startup_info("Install menu item added")

            def show_user_mode_dialog():
                from UserModeDialog import UserModeDialog
                from aqt import mw

                mw.userModeDialog = UserModeDialog()
                mw.userModeDialog.show()

            add_ankibrain_menu_item("Switch User Mode...", show_user_mode_dialog)
            boot_logger.startup_info("User mode switch menu item added")

    boot_logger.startup_info("Local mode loading completed")
    log_startup_phase("AnkiBrain Local Mode Loaded")


def load_ankibrain_server_mode():
    """Load AnkiBrain in server mode - creates AnkiBrain instance configured for server usage."""
    print("Loading AnkiBrain in Regular (Server) Mode...")
    boot_logger.startup_info("Entering server mode loading sequence")
    log_startup_phase("Loading AnkiBrain Server Mode")

    with PerformanceTimer(boot_logger, "import_server_mode_dependencies"):
        from AnkiBrainModule import AnkiBrain
        from util import UserMode

    with PerformanceTimer(boot_logger, "create_server_mode_instance"):
        boot_logger.startup_info("Creating AnkiBrain instance in SERVER mode")
        mw.ankiBrain = AnkiBrain(user_mode=UserMode.SERVER)
        boot_logger.startup_info("Server mode AnkiBrain instance created and assigned")

    boot_logger.startup_info("Server mode loading completed")
    log_startup_phase("AnkiBrain Server Mode Loaded")


# TODO: this doesn't actually work, none of the menu items get removed. Method is not being used.
def unload_ankibrain():
    print("Unloading AnkiBrain...")
    if hasattr(mw, "ankiBrain") and mw.ankiBrain is not None:
        # mw.ankiBrain.sidePanel.close()
        print("Destroying mw AnkiBrain instance...")
        mw.ankiBrain.stop_main()
        mw.ankiBrain = None

    if hasattr(mw, "settingsManager") and mw.settingsManager is not None:
        print("Destroying mw SettingsManager instance...")
        mw.settingsManager = None

    from AnkiBrainModule import remove_ankibrain_menu_actions

    remove_ankibrain_menu_actions()


def reload_ankibrain():
    showInfo("Please restart Anki to allow AnkiBrain to update.")
