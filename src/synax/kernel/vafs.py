"""SYNAX-OS Kernel — Virtual Agent File System (VAFS).

Provides a POSIX-like virtual filesystem exposing:
- /proc/agents/ (Active processes & PIDs)
- /dev/tools/   (Hardware & API tools exposed as virtual devices)
- /sys/         (Kernel parameters, scheduler metrics & memory)
- /var/log/     (Live telemetry logs)
"""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional


class VirtualNode:
    """A node inside the Virtual Agent File System."""

    def __init__(
        self,
        name: str,
        is_directory: bool = False,
        content_provider: Optional[Callable[[], str]] = None,
    ) -> None:
        self.name = name
        self.is_directory = is_directory
        self._content_provider = content_provider
        self.children: Dict[str, VirtualNode] = {}

    def read(self) -> str:
        """Read node content."""
        if self.is_directory:
            return json.dumps(list(self.children.keys()), indent=2)
        if self._content_provider:
            return self._content_provider()
        return ""


class VirtualAgentFileSystem:
    """Hierarchical VAFS implementation."""

    def __init__(self) -> None:
        self.root = VirtualNode("/", is_directory=True)
        self.mkdir("/proc")
        self.mkdir("/proc/agents")
        self.mkdir("/dev")
        self.mkdir("/dev/tools")
        self.mkdir("/sys")
        self.mkdir("/var")
        self.mkdir("/var/log")

    def mkdir(self, path: str) -> None:
        """Create a virtual directory path."""
        parts = [p for p in path.strip("/").split("/") if p]
        curr = self.root
        for part in parts:
            if part not in curr.children:
                curr.children[part] = VirtualNode(part, is_directory=True)
            curr = curr.children[part]

    def mount_file(self, path: str, provider: Callable[[], str]) -> None:
        """Mount a dynamic content provider as a virtual file."""
        parts = [p for p in path.strip("/").split("/") if p]
        filename = parts[-1]
        dir_path = "/" + "/".join(parts[:-1])
        self.mkdir(dir_path)

        # Traverse to target dir
        curr = self.root
        for part in parts[:-1]:
            curr = curr.children[part]
        curr.children[filename] = VirtualNode(filename, is_directory=False, content_provider=provider)

    def read_file(self, path: str) -> str:
        """Read virtual file contents."""
        parts = [p for p in path.strip("/").split("/") if p]
        curr = self.root
        for part in parts:
            if part not in curr.children:
                raise FileNotFoundError(f"VAFS: No such file or directory: {path}")
            curr = curr.children[part]
        return curr.read()

    def list_dir(self, path: str) -> List[str]:
        """List files and subdirectories under virtual path."""
        parts = [p for p in path.strip("/").split("/") if p]
        curr = self.root
        for part in parts:
            if part not in curr.children:
                raise FileNotFoundError(f"VAFS: No such directory: {path}")
            curr = curr.children[part]
        if not curr.is_directory:
            raise NotADirectoryError(f"VAFS: Not a directory: {path}")
        return list(curr.children.keys())
