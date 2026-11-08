"""Execute real runtimes and compilers; no shell or in-process evaluation."""

import shutil
import subprocess
import sys
from pathlib import Path

EXECUTABLES = {
    "py": sys.executable,
    "js": "node",
    "go": "go",
    "rb": "ruby",
    "ps": "pwsh",
    "rs": "rustc",
    "php": "php",
    "lua": "lua",
    "pl": "perl",
    "java": "java",
    "hs": "ghc",
    "c": "cc",
    "kt": "kotlinc",
}


def available(language):
    return shutil.which(EXECUTABLES[language]) is not None


def command_for(language, source, workdir):
    source = str(Path(source).resolve())
    executable = shutil.which(EXECUTABLES[language])
    if executable is None:
        raise RuntimeError(f"missing runtime for {language}: {EXECUTABLES[language]}")
    if language in ("go", "rs", "hs", "c", "kt"):
        suffix = ".exe" if sys.platform == "win32" else ""
        binary = str(Path(workdir).resolve() / (language + "-bin" + suffix))
        if language == "go":
            command = [executable, "build", "-o", binary, source]
        elif language == "rs":
            command = [
                executable,
                "--edition=2021",
                "--crate-name",
                "lda",
                source,
                "-o",
                binary,
            ]
        elif language == "hs":
            command = [
                executable,
                "-v0",
                "-O0",
                "-fforce-recomp",
                "-outputdir",
                str(Path(workdir).resolve()),
                source,
                "-o",
                binary,
            ]
        elif language == "c":
            command = [executable, "-std=c11", "-O0", source, "-o", binary]
        else:
            binary = str(Path(workdir).resolve() / "kt-bin.jar")
            command = [executable, source, "-include-runtime", "-d", binary, "-nowarn"]
        subprocess.run(command, check=True, timeout=120)
        if language == "kt":
            java = shutil.which("java")
            if java is None:
                raise RuntimeError("Kotlin JVM execution requires java")
            return [java, "-jar", binary]
        return [binary]
    flags = {
        "py": [],
        "js": [],
        "rb": [],
        "php": ["-n"],
        "lua": [],
        "pl": [],
        "java": [],
        "ps": ["-NoLogo", "-NoProfile", "-NonInteractive", "-File"],
    }
    return [executable, *flags[language], source]


def execute(command, args=(), cwd=None, *, input_bytes=None):
    result = subprocess.run(
        [*command, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        input=input_bytes,
        timeout=30,
    )
    if result.returncode:
        raise RuntimeError(
            f"{command[0]} exited {result.returncode}:\n"
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout
