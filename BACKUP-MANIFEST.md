# StrongerFX / MemeFX backup manifest

This existing private-adjacent repository contains the older MemeFX implementation and related launch work. Its remote remains `smartpage/strongerfx-mcp` for continuity.

## Included

- MemeFX membership, catalog, API, MCP and Actor source changes.
- Campaign, launch, creative, research and test files that belong to the MemeFX implementation.
- Reviewable rendered media and package archives where they are useful as creative exports.

## Excluded by design

- Standalone source audio and sidecars. Audio is stored on Contabo at `/data/memefx/media` per the workspace handoff.
- Local credentials, `.env*` except `.env.example`, storage directories, dependency trees, caches, browser state, Python bytecode and runtime databases/journals.

## Scope note

The pending changes in this workspace were inspected as MemeFX work and are being committed to the existing `strongerfx-mcp` repository. No unrelated repository or directory was imported.
