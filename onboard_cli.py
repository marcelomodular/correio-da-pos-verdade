"""Onboarding CLI for Politicagem.

This script introduces the project, installs dependencies, and can create
an optional desktop shortcut using the Politicagem icon.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
ELECTRON_DIR = ROOT_DIR / "electron-app"
ICON_ICO_PATH = ELECTRON_DIR / "assets" / "politicagem-p.ico"
LAUNCHER_BAT_PATH = ROOT_DIR / "politicagem-desktop.bat"

ASCII_ART = r"""
PPPP   OOO   L      III  TTTTT  III   CCCC    A     GGG   EEEE  M   M
P   P O   O  L       I     T     I   C       A A   G      E     MM MM
PPPP  O   O  L       I     T     I   C      AAAAA  G GGG  EEE   M M M
P     O   O  L       I     T     I   C      A   A  G   G  E     M   M
P      OOO   LLLLL  III    T    III   CCCC  A   A   GGG   EEEE  M   M
"""


def log(message: str) -> None:
    print(message, flush=True)


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[S/n]" if default else "[s/N]"
    valid_yes = {"s", "sim", "y", "yes"}
    valid_no = {"n", "nao", "no"}

    while True:
        answer = input(f"{prompt} {suffix}: ").strip().lower()
        if not answer:
            return default
        if answer in valid_yes:
            return True
        if answer in valid_no:
            return False
        log("Resposta invalida. Digite s ou n.")


def run_command(command: list[str], cwd: Path | None = None) -> None:
    pretty = " ".join(command)
    log(f"\n> Executando: {pretty}")
    subprocess.run(command, cwd=str(cwd) if cwd else None, check=True)


def explain_project() -> None:
    log(ASCII_ART)
    log("Politicagem: agregador de noticias RSS com visual de jornal classico.")
    log("- Nao armazena noticias em banco de dados.")
    log("- Busca os feeds RSS em tempo real, por requisicao.")
    log("- O foco e centralizar fontes em uma leitura unica e rapida.")


def install_python_dependencies() -> None:
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=ROOT_DIR)


def install_electron_dependencies() -> None:
    npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm_cmd:
        raise RuntimeError("npm nao encontrado. Instale Node.js para continuar.")
    run_command([npm_cmd, "install"], cwd=ELECTRON_DIR)


def write_launcher_bat() -> None:
    content = """@echo off
cd /d "%~dp0electron-app"
if not exist node_modules (
  echo Dependencias do Electron nao encontradas.
  echo Rode onboarding novamente e instale o Electron.
)
npm start
"""
    LAUNCHER_BAT_PATH.write_text(content, encoding="utf-8")


def powershell_escape(value: str) -> str:
    return value.replace("'", "''")


def create_desktop_shortcut() -> None:
    if os.name != "nt":
        log("Criacao de atalho automatico disponivel apenas no Windows.")
        return

    if not ICON_ICO_PATH.exists():
        raise FileNotFoundError(f"Icone nao encontrado: {ICON_ICO_PATH}")

    write_launcher_bat()

    desktop_dir = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    if not desktop_dir.exists():
        raise FileNotFoundError(f"Area de Trabalho nao encontrada: {desktop_dir}")

    shortcut_path = desktop_dir / "Politicagem.lnk"
    target_path = LAUNCHER_BAT_PATH

    script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{powershell_escape(str(shortcut_path))}')
$Shortcut.TargetPath = '{powershell_escape(str(target_path))}'
$Shortcut.WorkingDirectory = '{powershell_escape(str(ROOT_DIR))}'
$Shortcut.IconLocation = '{powershell_escape(str(ICON_ICO_PATH))},0'
$Shortcut.Description = 'Politicagem - agregador RSS sem armazenamento local'
$Shortcut.Save()
"""

    run_command(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            script,
        ]
    )


def run_onboarding(auto: bool) -> None:
    explain_project()

    do_python = True
    do_electron = True
    do_shortcut = os.name == "nt"

    if not auto:
        do_python = ask_yes_no("Instalar dependencias Python agora?", default=True)
        do_electron = ask_yes_no("Instalar dependencias Electron agora?", default=True)
        if os.name == "nt":
            do_shortcut = ask_yes_no("Criar atalho na Area de Trabalho?", default=True)

    if do_python:
        install_python_dependencies()
        log("[OK] Dependencias Python instaladas.")

    if do_electron:
        install_electron_dependencies()
        log("[OK] Dependencias Electron instaladas.")

    if do_shortcut:
        create_desktop_shortcut()
        log("[OK] Atalho da Area de Trabalho criado com o icone do Politicagem.")

    log("\nOnboarding concluido.")
    log("Para abrir o desktop app manualmente: cd electron-app && npm start")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Onboarding CLI do Politicagem")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Executa tudo sem perguntas (instala Python, Electron e atalho no Windows).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        run_onboarding(auto=args.auto)
    except subprocess.CalledProcessError as exc:
        log(f"\n[ERRO] Falha ao executar comando (codigo {exc.returncode}).")
        raise SystemExit(exc.returncode) from exc
    except Exception as exc:
        log(f"\n[ERRO] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
