"""System monitor — collects CPU, memory, and disk usage."""

from __future__ import annotations

import platform

import psutil


class SystemMonitor:
    """Collects system resource information."""

    async def get_status(self, **kwargs) -> dict:
        """Get current system resource usage."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "system": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "hostname": platform.node(),
                "python_version": platform.python_version(),
            },
            "cpu": {
                "percent": cpu_percent,
                "count": psutil.cpu_count(),
                "count_logical": psutil.cpu_count(logical=True),
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent": memory.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent,
            },
        }
