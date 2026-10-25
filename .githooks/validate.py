#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

REQUIRED_KEYS = (
    "general",
    "gaps",
    "window_effects",
    "window_behavior",
    "workspaces",
    "window_rules",
    "keybindings",
)

CONFLICT_RE = re.compile(r"^(?:<{7}|>{7})(?: |$)", re.MULTILINE)

PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN " + r"(?:RSA|OPENSSH|EC|DSA|PGP) " + r"PRIVATE KEY-----"
)
SECRET_PATTERNS = (
    ("private key", PRIVATE_KEY_RE),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{36,}\b")),
    ("OpenAI key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    (
        "hardcoded credential",
        re.compile(
            r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\b"
            r"\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        ),
    ),
)

SENSITIVE_NAMES = {
    ".env",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".bmp",
    ".pdf",
    ".zip",
    ".gz",
    ".7z",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
}


def read_text(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if b"\x00" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def validate_glazewm(path, document, errors, repo_root):
    if not isinstance(document, dict):
        errors.append(f"{path}: la raiz del YAML debe ser un mapa")
        return

    missing = [key for key in REQUIRED_KEYS if key not in document]
    if missing:
        errors.append(f"{path}: faltan claves obligatorias: {', '.join(missing)}")

    general = document.get("general")
    if not isinstance(general, dict) or not isinstance(
        general.get("startup_commands"), list
    ):
        errors.append(f"{path}: general.startup_commands debe ser una lista")

    gaps = document.get("gaps")
    if not isinstance(gaps, dict):
        errors.append(f"{path}: gaps debe ser un mapa")
    else:
        if "inner_gap" not in gaps:
            errors.append(f"{path}: falta gaps.inner_gap")
        outer = gaps.get("outer_gap")
        if not isinstance(outer, dict) or not all(
            side in outer for side in ("top", "right", "bottom", "left")
        ):
            errors.append(
                f"{path}: gaps.outer_gap debe definir top, right, bottom y left"
            )

    effects = document.get("window_effects")
    focused = effects.get("focused_window") if isinstance(effects, dict) else None
    transparency = (
        focused.get("transparency") if isinstance(focused, dict) else None
    )
    if not isinstance(transparency, dict) or not isinstance(
        transparency.get("enabled"), bool
    ):
        errors.append(
            f"{path}: window_effects.focused_window.transparency.enabled debe ser booleano"
        )

    rules = document.get("window_rules")
    if not isinstance(rules, list):
        errors.append(f"{path}: window_rules debe ser una lista")
    else:
        for index, rule in enumerate(rules):
            if not isinstance(rule, dict):
                errors.append(f"{path}: window_rules[{index}] debe ser un mapa")
                continue
            if not isinstance(rule.get("commands"), list):
                errors.append(
                    f"{path}: window_rules[{index}].commands debe ser una lista"
                )
            if not isinstance(rule.get("match"), list):
                errors.append(
                    f"{path}: window_rules[{index}].match debe ser una lista"
                )

    for key in ("workspaces", "keybindings"):
        if not isinstance(document.get(key), list):
            errors.append(f"{path}: {key} debe ser una lista")

    seen_scripts = set()
    for keybinding in document.get("keybindings", []):
        if not isinstance(keybinding, dict):
            continue
        for command in keybinding.get("commands", []):
            if not isinstance(command, str):
                continue
            for script_name in re.findall(r"([\w.-]+\.ps1)", command):
                if script_name in seen_scripts:
                    continue
                seen_scripts.add(script_name)
                script_path = os.path.join(repo_root, "glazewm", script_name)
                if not os.path.isfile(script_path):
                    errors.append(
                        f"{path}: script referenciado no existe: glazewm/{script_name}"
                    )


def validate_powershell_syntax(path, rel_path, errors):
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if not powershell:
        return

    env = os.environ.copy()
    env["GLAZEWM_VALIDATE_PS1"] = path
    script = (
        "$tokens = $null; $errs = $null; "
        "[System.Management.Automation.Language.Parser]::ParseFile("
        "$env:GLAZEWM_VALIDATE_PS1, [ref]$tokens, [ref]$errs) | Out-Null; "
        "if ($errs.Count -gt 0) { "
        "$errs | ForEach-Object { Write-Output $_.Message }; exit 1 }"
    )
    result = subprocess.run(
        [powershell, "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        errors.append(f"{rel_path}: sintaxis PowerShell invalida: {detail}")


def validate_yaml(path, text, errors, repo_root):
    try:
        import yaml
    except ImportError:
        errors.append(f"{path}: falta PyYAML (python -m pip install pyyaml)")
        return

    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        errors.append(f"{path}: YAML invalido: {exc}")
        return

    parts = path.replace("\\", "/").split("/")
    if parts[-1] == "config.yaml" and "glazewm" in parts:
        validate_glazewm(path, document, errors, repo_root)


def validate_json(path, text, errors):
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(
            f"{path}: JSON invalido en linea {exc.lineno}, columna {exc.colno}: {exc.msg}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--files-from")
    parser.add_argument("--files", nargs="*", default=[])
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)

    files = list(args.files)
    if args.files_from:
        with open(args.files_from, "r", encoding="utf-8") as handle:
            files.extend(line.strip() for line in handle if line.strip())

    seen = set()
    ordered = []
    for rel_path in files:
        rel_path = rel_path.replace("\\", "/")
        if rel_path not in seen:
            seen.add(rel_path)
            ordered.append(rel_path)

    errors = []
    checked = 0

    for rel_path in ordered:
        abs_path = os.path.join(repo_root, rel_path.replace("/", os.sep))
        if not os.path.isfile(abs_path):
            continue

        name = os.path.basename(rel_path)
        extension = os.path.splitext(name)[1].lower()

        if name in SENSITIVE_NAMES:
            errors.append(f"{rel_path}: archivo sensible (posible secreto)")
            continue

        if extension == ".log":
            errors.append(f"{rel_path}: no se permiten archivos .log")
            continue

        if extension in BINARY_EXTENSIONS:
            continue

        text = read_text(abs_path)
        if text is None:
            continue

        checked += 1

        if CONFLICT_RE.search(text):
            errors.append(f"{rel_path}: contiene marcadores de conflicto")

        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel_path}: posible secreto detectado ({label})")

        if extension in (".yaml", ".yml"):
            validate_yaml(rel_path, text, errors, repo_root)
        elif extension == ".json":
            validate_json(rel_path, text, errors)
        elif extension == ".ps1":
            validate_powershell_syntax(abs_path, rel_path, errors)

    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        print(
            f"validacion: fallida ({len(errors)} error(es), {checked} archivo(s) revisado(s))",
            file=sys.stderr,
        )
        return 1

    print(f"validacion: OK ({checked} archivo(s) revisado(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
