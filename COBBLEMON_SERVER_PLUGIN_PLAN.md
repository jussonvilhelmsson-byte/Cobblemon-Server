# Cobblemon Server Plugin Plan (MC 1.21.1, Latest Cobblemon)

This is a practical plugin/mod stack and implementation plan for a **survival Cobblemon server**.
Because Cobblemon servers are usually Fabric/NeoForge-based, these are mostly **server-side mods** (often called plugins by server owners).

## 0) Baseline assumptions

- Minecraft: **1.21.1**
- Cobblemon: **latest available for 1.21.1**
- Loader: **Fabric** (recommended for broader server tooling)
- Java: version required by your chosen MC/Cobblemon build

> Before final deployment, confirm each mod's exact game/version compatibility on Modrinth/CurseForge for your specific Cobblemon build.

---

## 1) Protection / Claims

### Recommended
- **FTB Chunks** (+ FTB Teams dependency): player/team land claims and chunk permissions.

### Why
- Fast setup, reliable for survival servers.
- Supports public/private claims and trust management.
- Good fit for bases, ranches, gyms, and shops.

### Server policy
- Set a starter claim limit (for example 50 chunks).
- Allow earning extra claim chunks via playtime, quests, or ranks.
- Disable claims in event worlds if needed.

---

## 2) Permissions / Staff Control

### Recommended
- **LuckPerms (Fabric)**

### Why
- Industry-standard permissions manager.
- Handles granular command access and staff role hierarchy.
- Essential with Cobblemon/admin commands to prevent abuse.

### Suggested groups
- `default`: survival commands only (home/spawn/trade/info)
- `helper`: chat moderation + report tools
- `mod`: temp punishments, rollback inspection
- `admin`: full admin commands except owner-only controls
- `owner`: all permissions

---

## 3) Economy / Shops

### Recommended core
- Pick one Fabric economy system and keep it simple:
  - **Lightman's Currency** (physical + account-based money/shop flow), or
  - **Numismatic Overhaul** (coin-based economy).

### Cobblemon flavor
- Rename/display currency as **Pokédollars** in chat, scoreboards, and shops.
- Add server shops for Poké Balls, medicine, and utility items.
- Keep ultra-rare Cobblemon content off easy pay-to-win loops.

### Economy guardrails
- Money sinks: breeding fees, daycare fees, tournament entry, repair costs.
- Anti-inflation: cap passive income sources and automate audits.

---

## 4) Trade / Social QoL

### Recommended
- **CobblemonExtras** (if updated for your target version).

### Why
- Adds multiplayer-friendly Cobblemon commands such as social and trade-oriented QoL.
- Reduces friction for player interactions.

### Policy tips
- Log all high-value trades.
- Add cooldowns for global broadcast commands.
- Require confirmation for irreversible trade actions.

---

## 5) In-game Info / Wiki Access

### Recommended
- **Cobblemon Wiki GUI** (or equivalent in-game dex/info UI).

### Why
- Reduces alt-tabbing and keeps players in-game.
- Better onboarding for new players learning species/moves/evolution lines.

### Good defaults
- Keep command access open to all players.
- Add short cooldowns if commands can be spammed.

---

## 6) Events / Progression Systems

### Recommended feature set
Use one or more server-side systems for:
- Gyms + badges
- Rotating outbreaks/spawns
- Raid/event bosses
- Daily/weekly quests
- Seasonal reward tracks

### Implementation strategy
- Start with one progression loop (for example gyms + weekly tournament).
- Add one recurring event loop (for example weekend outbreak rotation).
- Add one retention loop (for example daily quest streak rewards).

### Balance guidance
- Avoid giving best-in-slot rewards from a single activity.
- Distribute rewards across PvE, collection, exploration, and social play.

---

## 7) Core Admin / Utility (must-have baseline)

### Required stack
- **Backups**: scheduled + offsite snapshots.
- **Logging/Rollback**: block and container history with rollback tools.
- **Moderation utilities**: inspect, mute, freeze/jail as needed.
- **Teleport/home tools**: `/spawn`, `/home`, `/tpa` with cooldowns.
- **Performance monitoring**: server profiler + alerting for TPS/RAM spikes.

### Operational policy
- Test restore procedure weekly.
- Keep at least 7 daily + 4 weekly backups.
- Track staff actions in immutable logs.

---

## Suggested “Day-1 Stable” stack

1. Cobblemon + dependencies
2. LuckPerms
3. FTB Chunks (+ Teams)
4. One economy mod (Lightman's Currency *or* Numismatic Overhaul)
5. CobblemonExtras
6. Cobblemon Wiki GUI
7. Backup + rollback/logging + performance tools

This gives immediate protection, moderation control, social features, and long-term progression scaffolding.

---

## 2-week rollout plan

### Week 1
- Deploy baseline stack.
- Configure permissions and claim limits.
- Launch starter shop + Pokédollar sinks.
- Enable social/trade QoL.

### Week 2
- Launch first gym track.
- Add one recurring outbreak/event.
- Publish seasonal roadmap (30–60 days).

---

## Minimal acceptance checklist

- [ ] No griefing possible in claimed chunks.
- [ ] Staff permissions validated with test accounts.
- [ ] Economy cannot be trivially duplicated/exploited.
- [ ] Trade actions are auditable.
- [ ] Players can access species info in-game.
- [ ] At least one recurring progression event is active.
- [ ] Backup restore test completed successfully.
