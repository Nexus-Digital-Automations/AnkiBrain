"""
Performance Logger - Comprehensive logging utility for AnkiBrain startup diagnosis

This module provides structured logging with performance timing, operation tracking,
and bottleneck identification specifically designed for diagnosing startup issues.

Usage:
    from performance_logger import get_performance_logger, log_startup_phase, PerformanceTimer

    logger = get_performance_logger('ModuleName')
    logger.startup_info('Module initializing', {'version': '1.0'})

    with PerformanceTimer(logger, 'expensive_operation'):
        # expensive operation here
        pass
"""

import logging
import time
import json
import threading
from contextlib import contextmanager
from typing import Dict, Any, Optional
from pathlib import Path
import os


class PerformanceFormatter(logging.Formatter):
    """
    Custom formatter that includes performance timing and structured data.
    Optimized for startup performance analysis.
    """

    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    def format(self, record):
        # Calculate time since logger initialization
        elapsed_time = (
            record.created - self.start_time
        ) * 1000  # Convert to milliseconds

        # Build structured log entry
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S.%f")[
                :-3
            ],  # Include milliseconds
            "elapsed_ms": round(elapsed_time, 2),
            "thread": record.thread,
            "process": record.process,
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }

        # Add performance metrics if available
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        if hasattr(record, "operation"):
            log_data["operation"] = record.operation

        if hasattr(record, "context"):
            log_data["context"] = record.context

        if hasattr(record, "memory_mb"):
            log_data["memory_mb"] = record.memory_mb

        # Format as structured JSON for easy analysis
        return json.dumps(log_data, separators=(",", ":"))


# Project-specific performance thresholds based on AnkiBrain requirements
PERFORMANCE_THRESHOLDS = {
    # Critical startup operations (high-priority bottlenecks)
    "wait_for_ready_message": 20000,  # 20s - ChatAI subprocess startup
    "create_ankibrain_instance": 5000,  # 5s - instance creation
    "load_ankibrain_main": 30000,  # 30s - total LOCAL mode startup
    "create_subprocess_exec": 10000,  # 10s - subprocess creation
    # Webview and UI operations
    "webview_initialization": 10000,  # 10s - side panel webview
    "create_ankibrain_menu": 1000,  # 1s - menu creation
    # Settings and configuration
    "initialize_settings_manager": 2000,  # 2s - settings load
    "setup_installation_dialog": 1000,  # 1s - dialog setup
    # Import and module loading operations
    "import_core_modules": 3000,  # 3s - core module imports
    "import_ankibrain_module": 2000,  # 2s - AnkiBrain module import
    "import_local_mode_dependencies": 1000,  # 1s - dependency imports
    "import_server_mode_dependencies": 1000,  # 1s - dependency imports
    # File operations and checks
    "check_installation_status": 1000,  # 1s - installation check
    "run_boot_checks": 2000,  # 2s - boot checks
    "setup_version_file": 500,  # 500ms - file operations
    # Default thresholds by operation patterns
    "setup_": 1000,  # 1s for setup operations
    "import_": 2000,  # 2s for import operations
    "create_": 3000,  # 3s for creation operations
    "initialize_": 2000,  # 2s for initialization operations
    "load_": 5000,  # 5s for loading operations
}


def get_threshold_for_operation(operation: str) -> float:
    """
    Get performance threshold for specific operation.
    Uses project-specific thresholds based on AnkiBrain performance requirements.
    """
    # Check for exact match first
    if operation in PERFORMANCE_THRESHOLDS:
        return PERFORMANCE_THRESHOLDS[operation]

    # Check for pattern matches (operations starting with specific prefixes)
    for pattern, threshold in PERFORMANCE_THRESHOLDS.items():
        if pattern.endswith("_") and operation.startswith(pattern):
            return threshold

    # Default threshold for unmatched operations (5 seconds as per requirements)
    return 5000


class PerformanceLogger:
    """
    Enhanced logger specifically designed for startup performance analysis.
    Provides timing capabilities, memory tracking, and structured output.
    """

    def __init__(self, name: str, log_file: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(f"AnkiBrain.Performance.{name}")
        self.logger.setLevel(logging.DEBUG)
        self.start_time = time.time()
        self._operation_stack = []
        self._timers: Dict[str, float] = {}

        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Console handler for immediate feedback
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                "[%(elapsed_ms)06.1fms] %(name)s: %(message)s"
            )
            console_handler.setFormatter(console_formatter)

            # File handler for detailed analysis
            if log_file is None:
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                log_file = log_dir / "ankibrain_performance.log"

            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(PerformanceFormatter())

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def _get_elapsed_ms(self) -> float:
        """Get milliseconds elapsed since logger creation."""
        return (time.time() - self.start_time) * 1000

    def _add_performance_data(self, record, **kwargs):
        """Add performance metadata to log record."""
        record.elapsed_ms = round(self._get_elapsed_ms(), 2)
        for key, value in kwargs.items():
            setattr(record, key, value)
        return record

    def startup_info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log startup-specific information with context."""
        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, "", 0, message, (), None
        )
        self._add_performance_data(record, context=context, operation="startup")
        self.logger.handle(record)

    def startup_warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log startup warnings that may indicate performance issues."""
        record = self.logger.makeRecord(
            self.logger.name, logging.WARNING, "", 0, message, (), None
        )
        self._add_performance_data(record, context=context, operation="startup")
        self.logger.handle(record)

    def startup_error(
        self, message: str, context: Optional[Dict[str, Any]] = None, exc_info=None
    ):
        """Log startup errors with full context."""
        record = self.logger.makeRecord(
            self.logger.name, logging.ERROR, "", 0, message, (), exc_info
        )
        self._add_performance_data(record, context=context, operation="startup")
        self.logger.handle(record)

    def timing_start(self, operation: str, context: Optional[Dict[str, Any]] = None):
        """Start timing an operation."""
        start_time = time.time()
        self._timers[operation] = start_time

        message = f"Starting {operation}"
        record = self.logger.makeRecord(
            self.logger.name, logging.DEBUG, "", 0, message, (), None
        )
        self._add_performance_data(record, operation=operation, context=context)
        self.logger.handle(record)

    def timing_end(self, operation: str, context: Optional[Dict[str, Any]] = None):
        """End timing an operation and log the duration."""
        if operation not in self._timers:
            self.startup_warning(f"No timer found for operation: {operation}")
            return 0

        duration = (time.time() - self._timers[operation]) * 1000  # Convert to ms
        del self._timers[operation]

        message = f"Completed {operation}"
        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, "", 0, message, (), None
        )
        self._add_performance_data(
            record, operation=operation, duration_ms=round(duration, 2), context=context
        )
        self.logger.handle(record)

        return duration

    def log_memory_usage(self, operation: str = "memory_check"):
        """Log current memory usage (if psutil is available)."""
        try:
            import psutil

            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024

            message = f"Memory usage: {memory_mb:.1f} MB"
            record = self.logger.makeRecord(
                self.logger.name, logging.DEBUG, "", 0, message, (), None
            )
            self._add_performance_data(
                record, operation=operation, memory_mb=round(memory_mb, 1)
            )
            self.logger.handle(record)

            return memory_mb
        except ImportError:
            self.startup_info("psutil not available for memory tracking")
            return None

    def log_bottleneck_warning(
        self, operation: str, duration_ms: float, threshold_ms: float = None
    ):
        """Log warning if operation exceeds performance threshold."""
        # Use project-specific thresholds if not explicitly provided
        if threshold_ms is None:
            threshold_ms = get_threshold_for_operation(operation)

        if duration_ms > threshold_ms:
            message = f"Performance bottleneck detected: {operation} took {duration_ms:.1f}ms (threshold: {threshold_ms}ms)"
            self.startup_warning(
                message,
                {
                    "operation": operation,
                    "duration_ms": duration_ms,
                    "threshold_ms": threshold_ms,
                    "performance_issue": True,
                },
            )


@contextmanager
def PerformanceTimer(
    logger: PerformanceLogger, operation: str, context: Optional[Dict[str, Any]] = None
):
    """
    Context manager for timing operations with automatic logging.

    Usage:
        with PerformanceTimer(logger, 'database_init'):
            initialize_database()
    """
    logger.timing_start(operation, context)
    start_time = time.time()

    try:
        yield
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.startup_error(
            f"Exception in {operation} after {duration_ms:.1f}ms: {str(e)}",
            context={"operation": operation, "duration_ms": duration_ms},
            exc_info=True,
        )
        raise
    finally:
        duration_ms = logger.timing_end(operation, context)
        # Check for performance bottlenecks using project-specific thresholds
        logger.log_bottleneck_warning(operation, duration_ms)


# Global logger instances for consistent usage across modules
_logger_instances: Dict[str, PerformanceLogger] = {}
_logger_lock = threading.Lock()


def get_performance_logger(
    name: str, log_file: Optional[str] = None
) -> PerformanceLogger:
    """
    Get or create a performance logger instance.
    Thread-safe singleton pattern per logger name.
    """
    with _logger_lock:
        if name not in _logger_instances:
            _logger_instances[name] = PerformanceLogger(name, log_file)
        return _logger_instances[name]


def log_startup_phase(phase: str, details: Optional[Dict[str, Any]] = None):
    """
    Convenience function to log major startup phases.
    Creates a 'StartupPhases' logger automatically.
    """
    logger = get_performance_logger("StartupPhases")
    logger.startup_info(f"Startup Phase: {phase}", details or {})


def log_system_info():
    """Log system information relevant to startup performance."""
    import platform
    import sys

    logger = get_performance_logger("SystemInfo")

    system_info = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_implementation": platform.python_implementation(),
        "current_working_directory": os.getcwd(),
    }

    logger.startup_info("System Information", system_info)
    logger.log_memory_usage("startup_system_info")


# Initialize logging immediately when module is imported
if __name__ != "__main__":
    log_startup_phase("PerformanceLogger module imported")
    log_system_info()
