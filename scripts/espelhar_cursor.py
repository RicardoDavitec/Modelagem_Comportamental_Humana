#!/usr/bin/env python3
"""Espelha .github/skills e .github/agents em .cursor/.

O Cursor procura skills e agentes em .cursor/. O conteudo canonico fica em
.github/. Este script aponta um no outro.

- Linux e macOS: link simbolico relativo.
- Windows sem WSL: junction (mklink /J). Nao exige administrador nem modo
  de desenvolvedor, ao contrario de um link simbolico de diretorio.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PARES = (
    (".cursor/skills", ".github/skills"),
    (".cursor/agents", ".github/agents"),
)


def repo_root() -> Path:
    aqui = Path(__file__).resolve()
    for pasta in (aqui.parent, *aqui.parents):
        if (pasta / ".git").exists():
            return pasta
    return aqui.parent.parent


def mesmo_destino(link: Path, alvo: Path) -> bool:
    try:
        return link.resolve() == alvo.resolve()
    except OSError:
        return False


def remover_link_antigo(link: Path) -> None:
    if link.is_symlink():
        link.unlink()
        return
    if os.name == "nt" and link.exists():
        # Junction aparece como diretorio. rmdir remove o junction, nao o alvo.
        subprocess.run(["cmd", "/c", "rmdir", str(link)], check=True)
        return
    if link.exists() and link.is_file():
        link.unlink()
        return
    if link.exists():
        raise SystemExit(
            f"{link} ja existe como diretorio real. Nao substitui para nao apagar conteudo."
        )


def criar_link(link: Path, alvo: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.exists() or link.is_symlink():
        if mesmo_destino(link, alvo):
            print(f"ok  {link.name} ja aponta para {alvo.name}")
            return
        remover_link_antigo(link)

    if os.name == "nt":
        concluido = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(alvo)],
            capture_output=True,
            text=True,
        )
        if concluido.returncode != 0:
            raise SystemExit(concluido.stderr.strip() or concluido.stdout.strip())
        print(f"junction  {link} -> {alvo}")
        return

    relativo = os.path.relpath(alvo, start=link.parent)
    link.symlink_to(relativo, target_is_directory=True)
    print(f"symlink  {link.name} -> {relativo}")


def main() -> None:
    raiz = repo_root()
    os.chdir(raiz)
    for destino, origem in PARES:
        alvo = raiz / origem
        if not alvo.is_dir():
            raise SystemExit(f"Origem ausente: {alvo}")
        criar_link(raiz / destino, alvo)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as erro:
        print(erro, file=sys.stderr)
        raise
