# Cobblemon Server Plugin Pack (MC 1.21.1)

This repository now includes an **actual plugin/mod installer** so you can bootstrap a Cobblemon server stack instead of manually hunting mods.

## What this gives you

- A script to download a curated server stack for:
  - Claims/protection
  - Permissions/staff controls
  - Economy
  - Trade/social QoL
  - In-game info
  - Core admin/performance utilities
- Config templates for fast startup.
- A KubeJS starter script for recurring event announcements.

## Install curated plugins/mods

From repository root:

```bash
python3 scripts/install_cobblemon_plugins.py --game-version 1.21.1 --loader fabric --mods-dir ./mods
```

Dry-run (no downloads):

```bash
python3 scripts/install_cobblemon_plugins.py --dry-run
```

Include alternative economy mod candidate:

```bash
python3 scripts/install_cobblemon_plugins.py --include-alt-economy
```

The installer writes a machine-readable report at:

- `server-pack/plugin-install-report.json`

## Next steps after install

1. Copy/adapt `config-templates/luckperms/bootstrap-commands.txt` into your LP setup workflow.
2. Enable KubeJS and drop `kubejs/server_scripts/cobblemon_events.js` into your server pack.
3. Start server once, then tune generated config files for each installed mod.

## Important

- Mod availability can change over time on Modrinth.
- If a slug has no compatible release for `fabric` + `1.21.1`, the installer logs it under `missing` in the report.
