#!/usr/bin/env python3
"""Install a curated Cobblemon server plugin/mod stack for Fabric 1.21.1.

This installer treats "plugins" as server-side mods for Cobblemon servers.
It resolves latest compatible versions from Modrinth and downloads jars
into ./mods (or a custom --mods-dir).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

MODRINTH_API = "https://api.modrinth.com/v2"
USER_AGENT = "cobblemon-server-plugin-installer/1.0"

STACK = {
    "protection_claims": ["ftb-chunks-fabric", "ftb-teams-fabric"],
    "permissions_staff": ["luckperms"],
    "economy_shops": ["lightmans-currency"],
    "trade_social_qol": ["cobblemonextras"],
    "ingame_info": ["cobblemon-wiki-gui"],
    "core_admin_utility": [
        "ledger",        # logging/rollback
        "ferrite-core",  # perf/memory
        "spark",         # profiler
        "simple-voice-chat",  # optional social utility
    ],
}

OPTIONAL_ALTERNATIVES = {
    "economy_shops": ["numismatic-overhaul"],
}


def http_get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def resolve_project_version(project_slug: str, game_version: str, loader: str):
    query = urllib.parse.urlencode(
        {
            "loaders": json.dumps([loader]),
            "game_versions": json.dumps([game_version]),
            "featured": "false",
        }
    )
    url = f"{MODRINTH_API}/project/{project_slug}/version?{query}"
    versions = http_get_json(url)
    if not versions:
        return None
    versions = sorted(versions, key=lambda v: v.get("date_published", ""), reverse=True)
    return versions[0]


def download_primary_file(version_obj: dict, mods_dir: pathlib.Path, dry_run: bool):
    files = version_obj.get("files", [])
    primary = next((f for f in files if f.get("primary")), files[0] if files else None)
    if not primary:
        raise RuntimeError(f"No downloadable file in version {version_obj.get('name')}")

    filename = primary["filename"]
    target = mods_dir / filename
    if dry_run:
        return {"filename": filename, "url": primary["url"], "path": str(target), "downloaded": False}

    req = urllib.request.Request(primary["url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as response:
        target.write_bytes(response.read())

    return {"filename": filename, "url": primary["url"], "path": str(target), "downloaded": True}


def iter_project_slugs(use_alt_economy: bool):
    for category, slugs in STACK.items():
        for slug in slugs:
            yield category, slug
        if use_alt_economy and category == "economy_shops":
            for alt in OPTIONAL_ALTERNATIVES["economy_shops"]:
                yield category, alt


def main() -> int:
    parser = argparse.ArgumentParser(description="Install curated Cobblemon server plugin/mod stack")
    parser.add_argument("--game-version", default="1.21.1")
    parser.add_argument("--loader", default="fabric")
    parser.add_argument("--mods-dir", default="mods")
    parser.add_argument("--include-alt-economy", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mods_dir = pathlib.Path(args.mods_dir)
    mods_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "game_version": args.game_version,
        "loader": args.loader,
        "mods_dir": str(mods_dir),
        "installed": [],
        "missing": [],
    }

    for category, slug in iter_project_slugs(args.include_alt_economy):
        try:
            version_obj = resolve_project_version(slug, args.game_version, args.loader)
        except urllib.error.HTTPError as exc:
            report["missing"].append({"category": category, "slug": slug, "reason": f"HTTP {exc.code}"})
            continue
        except Exception as exc:  # noqa: BLE001
            report["missing"].append({"category": category, "slug": slug, "reason": str(exc)})
            continue

        if not version_obj:
            report["missing"].append(
                {
                    "category": category,
                    "slug": slug,
                    "reason": f"No {args.loader}/{args.game_version} version found",
                }
            )
            continue

        try:
            file_result = download_primary_file(version_obj, mods_dir, dry_run=args.dry_run)
        except Exception as exc:  # noqa: BLE001
            report["missing"].append({"category": category, "slug": slug, "reason": str(exc)})
            continue

        report["installed"].append(
            {
                "category": category,
                "slug": slug,
                "version": version_obj.get("version_number"),
                "name": version_obj.get("name"),
                "project_id": version_obj.get("project_id"),
                "file": file_result,
            }
        )

    print(json.dumps(report, indent=2))
    lock_path = pathlib.Path("server-pack") / "plugin-install-report.json"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    return 0 if report["installed"] else 1


if __name__ == "__main__":
    sys.exit(main())
