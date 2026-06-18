from __future__ import annotations

from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOT = ROOT / "docs" / "voice_trait_carryover_flow.dot"
OUT = ROOT / "docs" / "voice_trait_carryover_flow.png"


def main() -> None:
    dot = shutil.which("dot")
    if not dot:
        raise SystemExit("Graphviz `dot` was not found on PATH.")
    subprocess.run(
        [dot, "-Tpng", "-Gdpi=160", str(DOT), "-o", str(OUT)],
        check=True,
    )
    print(OUT)


if __name__ == "__main__":
    main()
