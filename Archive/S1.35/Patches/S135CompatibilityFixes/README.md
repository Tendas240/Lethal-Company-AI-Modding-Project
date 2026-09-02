# S1.35 Compatibility Fixes

Project-local plugin for the Tendas Lethal Company profile.

- Keeps landed ship-door hydraulic power at 100% while at least one living controlled player is actually inside the ship.
- If all living players are outside and the door is closed, preserves vanilla hydraulic drain so the door reopens instead of causing a permanent lockout.
- Adds DoorAudit/DoorFailsafe diagnostics.
- Patches EnemyScan 1.2.1 so the terminal command `enemies` lists all active EnemyAI objects, not only enemies that have ScanNodeProperties.

This is a local mod. When importing the accompanying r2z into Gale, enable **Advanced options -> Import all files** so the DLL embedded in the profile is extracted.
