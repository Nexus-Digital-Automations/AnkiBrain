import asyncio
import atexit
import json
import platform
import subprocess
import time

from InterprocessCommand import InterprocessCommand
from performance_logger import (
    get_performance_logger,
    PerformanceTimer,
    log_startup_phase,
)


class ExternalScriptManager:
    def __init__(self, python_path, script_path):
        """Initialize ExternalScriptManager with comprehensive performance logging."""
        self.python_path = python_path
        self.script_path = script_path
        self.process = None
        self.lock = asyncio.Lock()

        # Create logger for external script management
        self.logger = get_performance_logger("ExternalScriptManager")
        self.logger.startup_info(
            "ExternalScriptManager initialized",
            {"python_path": python_path, "script_path": script_path},
        )

    async def start(self):
        """Start external Python subprocess - MAJOR PERFORMANCE BOTTLENECK."""
        startup_start_time = time.time()
        self.logger.startup_info(
            "Starting external Python subprocess - CRITICAL BOTTLENECK"
        )
        log_startup_phase("ExternalScriptManager Subprocess Start")

        with PerformanceTimer(self.logger, "setup_subprocess_parameters"):
            creationflags = 0
            if platform.system() == "Windows":
                creationflags = subprocess.CREATE_NO_WINDOW
                self.logger.startup_info(
                    "Windows detected - using CREATE_NO_WINDOW flag"
                )
            else:
                self.logger.startup_info(
                    f"Platform: {platform.system()} - no special flags"
                )

        with PerformanceTimer(self.logger, "create_subprocess_exec"):
            self.logger.startup_info(
                "Creating subprocess with asyncio.create_subprocess_exec",
                {
                    "python_path": self.python_path,
                    "script_path": self.script_path,
                    "memory_limit_gb": 1,
                },
            )

            subprocess_start_time = time.time()
            self.process = await asyncio.create_subprocess_exec(
                self.python_path,
                self.script_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=creationflags,
                limit=1024 * 1024 * 1024 * 1024,  # 1 GB
            )
            subprocess_creation_time = (time.time() - subprocess_start_time) * 1000

            self.logger.startup_info(
                "Subprocess created successfully",
                {
                    "creation_time_ms": round(subprocess_creation_time, 2),
                    "process_pid": self.process.pid if self.process else "unknown",
                },
            )

        with PerformanceTimer(self.logger, "register_exit_handler"):
            atexit.register(self.process.terminate)
            self.logger.startup_info("Exit handler registered for subprocess cleanup")

        # Wait for the ready message from external script - MAJOR BOTTLENECK
        with PerformanceTimer(self.logger, "wait_for_ready_message"):
            self.logger.startup_info(
                "Waiting for ChatAI ready message - BOTTLENECK EXPECTED"
            )

            ready_wait_start = time.time()
            try:
                ready_msg = await asyncio.wait_for(
                    self.process.stdout.readline(), timeout=60.0  # 60 second timeout
                )
                ready_wait_time = (time.time() - ready_wait_start) * 1000

                self.logger.startup_info(
                    "Ready message received",
                    {"wait_time_ms": round(ready_wait_time, 2)},
                )

                # Log bottleneck if ready message took too long
                if ready_wait_time > 10000:  # 10 seconds
                    self.logger.startup_error(
                        "Ready message bottleneck detected",
                        {"wait_time_ms": ready_wait_time, "threshold_ms": 10000},
                    )

            except asyncio.TimeoutError:
                self.logger.startup_error(
                    "CRITICAL: Ready message timeout - subprocess failed to start"
                )
                raise Exception(
                    "ChatAI module failed to start - timeout waiting for ready message"
                )

        with PerformanceTimer(self.logger, "parse_ready_message"):
            try:
                ready_data = json.loads(ready_msg.decode().strip())
                self.logger.startup_info("Ready message parsed", {"data": ready_data})

                if ready_data["status"] == "success":
                    total_startup_time = (time.time() - startup_start_time) * 1000
                    self.logger.startup_info(
                        "ChatAI module startup completed successfully",
                        {"total_time_ms": round(total_startup_time, 2)},
                    )
                    log_startup_phase(
                        "ExternalScriptManager Startup Success",
                        {"total_time_ms": round(total_startup_time, 2)},
                    )

                    # Log major bottleneck if total startup was very slow
                    if total_startup_time > 30000:  # 30 seconds
                        self.logger.startup_error(
                            "MAJOR BOTTLENECK: External script startup exceeded 30s",
                            {
                                "total_time_ms": total_startup_time,
                                "threshold_ms": 30000,
                            },
                        )
                else:
                    self.logger.startup_error(
                        "ChatAI module startup failed", {"ready_data": ready_data}
                    )
                    raise Exception(f"Error starting ChatAI module: {ready_data}")

            except json.JSONDecodeError as e:
                self.logger.startup_error(
                    "Failed to parse ready message JSON",
                    {"raw_message": ready_msg.decode().strip(), "json_error": str(e)},
                )
                raise Exception(
                    f"Invalid ready message from ChatAI module: {ready_msg.decode().strip()}"
                )

    async def stop(self):
        if self.process is not None:
            self.process.terminate()
            await self.process.wait()

    def terminate_sync(self):
        if self.process is None:
            return

        print("Terminating ChatAI subprocess...")
        self.process.terminate()

    async def call(self, input_data: dict[str, str]) -> dict[str, str]:
        try:
            data_str: str = json.dumps(input_data)
            async with self.lock:  # Acquire lock before writing and draining
                self.process.stdin.write(data_str.encode() + b"\n")
                await self.process.stdin.drain()

            output_str = await self.process.stdout.readline()
            async with self.lock:  # Acquire lock again before loading the json
                output_data = json.loads(output_str.decode().strip())

            # Handle module error.
            if output_data["cmd"] == InterprocessCommand.SUBMODULE_ERROR.value:
                error_msg = output_data["data"]["error"]
                raise Exception(error_msg)

            return output_data
        except Exception as e:
            raise Exception(str(e))
            # print(e)
            # return {
            #     'cmd': 'SUBMODULE_ERROR',
            #     'data': {
            #         'error': str(e)
            #     }
            # }
