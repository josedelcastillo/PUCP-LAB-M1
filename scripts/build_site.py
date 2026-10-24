"""Genera el sitio estático de la aplicación para un entorno dado."""

import argparse
import html
import json
from datetime import UTC, datetime
from pathlib import Path

PROJECT_NAME = "PUCP-LAB-M1"

BACKGROUNDS = {
    "local": "#1e3a8a",
    "staging": "#6b7280",
    "production": "#15803d",
}

TEMPLATE = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{project} · {env}</title>
  <style>
    html, body {{ margin: 0; height: 100%; }}
    body {{
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      background: {background}; color: #ffffff;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; text-align: center;
    }}
    h1 {{ font-size: clamp(2rem, 6vw, 4rem); margin: 0 0 1rem; }}
    .version {{ font-size: clamp(3rem, 12vw, 8rem); font-weight: 800; line-height: 1; }}
    .env {{
      font-size: clamp(1.5rem, 5vw, 3rem); text-transform: uppercase;
      letter-spacing: .2em; margin-top: 1rem;
    }}
    .built {{ margin-top: 2rem; opacity: .8; font-size: .9rem; }}
  </style>
</head>
<body>
  <h1>{project}</h1>
  <div class="version">{version}</div>
  <div class="env">{env}</div>
  <div class="built">built at {built_at}</div>
</body>
</html>
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Versión a publicar, p. ej. v1.0.0")
    parser.add_argument("--env", required=True, choices=sorted(BACKGROUNDS), help="Entorno destino")
    parser.add_argument("--output", default="site", help="Directorio de salida (default: site)")
    return parser.parse_args(argv)


def build(version: str, env: str, output: Path) -> None:
    built_at = datetime.now(UTC).isoformat(timespec="seconds")
    output.mkdir(parents=True, exist_ok=True)

    page = TEMPLATE.format(
        project=PROJECT_NAME,
        version=html.escape(version),
        env=html.escape(env),
        background=BACKGROUNDS[env],
        built_at=built_at,
    )
    (output / "index.html").write_text(page, encoding="utf-8")

    metadata = {"version": version, "env": env, "built_at": built_at}
    (output / "version.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    build(args.version, args.env, Path(args.output))
    print(f"Sitio generado en {args.output}/ ({args.version}, {args.env})")


if __name__ == "__main__":
    main()
