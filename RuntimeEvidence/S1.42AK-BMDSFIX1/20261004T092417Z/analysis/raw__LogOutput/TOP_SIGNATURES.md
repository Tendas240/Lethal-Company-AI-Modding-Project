# Top normalized runtime signatures

Every log event was processed. Dynamic GUID/hex/numeric values are normalized for aggregation.
Full normalized signature coverage is stored in `signatures/` and indexed by `SIGNATURES_MANIFEST.json`.

| Count | Level | Source | Lines | Normalized event |
|---:|---|---|---:|---|
| 3863 | Error | Unity Log | 35484-55092 | NullReferenceException ↩ Stack trace: ↩ UnityEngine.Transform.get_position () (at <<hex>>:IL_0000) ↩ LCOffice.Components.ElevatorStorage.LateUpdate () (at <<hex>>:IL_0011) |
| 1562 | Error | Unity Log | 19210-22359 | No more space in Reflection Probe Atlas. To solve this issue, increase the size of the Reflection Probe Atlas in the HDRP settings. |
| 1193 | Warning | Coroner | 11744-35356 | Could not access dying player: Collider was not a player! |
| 1193 | Warning | Coroner | 11745-35357 | Could not access dying player: Index not assigned! |
| 996 | Debug | Coroner | 11746-35358 | Handling Out of Bounds death... |
| 479 | Debug | Coroner | 12064-35138 | Querying target player parameters pre-death... |
| 479 | Debug | Coroner | 12065-35139 | Query successful!True |
| 436 | Debug | Coroner | 32071-35140 | Handling Old Bird (Stomp) damage... |
| 436 | Warning | Coroner | 32072-35141 | Could not access dying player: Player is still alive! |
| 421 | Error | Unity Log | 24277-25124 | RuntimeNavMeshBuilder: Source mesh Cube is skipped because it does not allow read access |
| 350 | Debug | TestAccountCore | 12359-24249 | Hazard injection: <int> matches, <int> hazards |
| 320 | Info | Unity Log | 28586-32577 | enemy rush index is <int>; current index <int> |
| 270 | Debug | ReXuvination | 14007-27381 | Optimised Collider layers in TerrainObstacleTrigger for Object: BreakTreeTrigger (UnityEngine.GameObject) |
| 198 | Debug | Coroner | 19832-21378 | Handling Spike Trap death... |
| 189 | Debug | LethalMin | 12827-35133 | Sprout Setting growth stage to <int> |
| 184 | Error | Unity Log | 24262-25119 | RuntimeNavMeshBuilder: Source mesh office_table_01 is skipped because it does not allow read access |
| 164 | Info | Unity Log | 8693-55207 | Item slot #<int> null?: True |
| 157 | Debug | ReXuvination | 11752-26028 | Optimised Collider layers in InteractTrigger for Object: InteractTrigger (UnityEngine.GameObject) |
| 157 | Info | Unity Log | 14519-55192 | Interact trigger destroying! name: InteractTrigger |
| 137 | Warning | Unity Log | 3728-4030 | The referenced script (UnityMeshSimplifier.LODBackupComponent) on this Behaviour is missing! |
| 134 | Error | Unity Log | 24266-25127 | RuntimeNavMeshBuilder: Source mesh Cube.002 is skipped because it does not allow read access |
| 124 | Error | Unity Log | 24265-25128 | RuntimeNavMeshBuilder: Source mesh Terminal.003 is skipped because it does not allow read access |
| 123 | Info | Unity Log | 10965-23099 | item awake: ChangableSuit(Clone); id: <int> |
| 123 | Warning | Unity Log | 10966-23100 | NetworkVariable is written to, but doesn't know its NetworkBehaviour yet. Are you modifying a NetworkVariable before the NetworkObject is spawned? |
| 123 | Debug | ScienceBirdTweaks | 10967-23101 | Parenting suits to ship! |
| 123 | Debug | ReXuvination | 11755-23521 | Optimised Collider layers in InteractTrigger for Object: ChangableSuit(Clone) (UnityEngine.GameObject) |
| 123 | Info | Unity Log | 14565-55189 | Interact trigger destroying! name: ChangableSuit(Clone) |
| 121 | Info | Unity Log | 29987-34725 | [Lethal Doors Fixed] Checking for enemies to apply damage |
| 97 | Debug | GeneralImprovements | 8825-37344 | Updated time display. |
| 96 | Info | Unity Log | 10912-22917 | Item sales percentages #<int>: <int> |
| 95 | Warning | Unity Log | 2184-4076 | The referenced script on this Behaviour (Game Object '') is missing! |
| 94 | Debug | ReXuvination | 8788-25986 | Optimised Collider layers in InteractTrigger for Object: Cube (UnityEngine.GameObject) |
| 94 | Info | Unity Log | 14670-55235 | Interact trigger destroying! name: Cube |
| 90 | Warning | Unity Log | 18562-33201 | PlayOneShot was called with a null AudioClip. |
| 86 | Info | ImmersiveScrap | 4239-4494 | Registered spawn rate for Vanilla to <int> |
| 86 | Info | ImmersiveScrap | 4240-4495 | Registered spawn rate for Custom to <int> |
| 86 | Warning | ainavt.lc.lethalconfig | 8275-8360 | Mod for assembly not found. |
| 80 | Warning | Unity Log | 14284-37330 | [Netcode] NetworkObject #<int> moved to the root because its parent NetworkObject #<int> is destroyed |
| 80 | Info | Unity Log | 29988-34738 | [Lethal Doors Fixed] White Pikmin_wYsu is in danger zone at position (<float>, <float>, <float>) |
| 80 | Info | Unity Log | 29989-34739 | Local client hit enemy White Pikmin_wYsu #<int> with force of 9999. |
| 80 | Info | LethalMin | 29990-34740 | White Pikmin_wYsu: Has Invincible mode when hit |
| 78 | Debug | ReXuvination | 16564-25240 | Optimised Collider layers in DoorLock for Object: Cube (UnityEngine.GameObject) |
| 75 | Warning | Unity Log | 14250-31868 | Failed to create agent because it is not close enough to the NavMesh |
| 73 | Info | Unity Log | 30338-34726 | [Lethal Doors Fixed] Bulbmin_7T62m is in danger zone at position (<float>, <float>, <float>) |
| 73 | Info | Unity Log | 30339-34727 | Local client hit enemy Bulbmin_7T62m #<int> with force of 9999. |
| 73 | Info | LethalMin | 30340-34728 | Bulbmin_7T62m: Has Invincible mode when hit |
| 64 | Debug | Coroner | 12167-35524 | Clearing cause of death for player <int> |
| 64 | Info | Unity Log | 19120-33174 | Is jetpack audio playing?: True |
| 61 | Debug | LethalMin | 12838-25879 | Spawning sprout <int> iteration(<int>) at: [(<float>, <float>, <float>), (<float>, <float>, <float>)] With type: Blue Pikmin odds:(<int>) rng: (<float> / <float>) |
| 61 | Debug | LethalMin | 12840-25881 | Blue Pikmin sprout initalized at ((<float>, <float>, <float>),(<float>, <float>, <float>)) |
| 61 | Info | Unity Log | 30344-34729 | [Lethal Doors Fixed] Bulbmin_irWwW is in danger zone at position (<float>, <float>, <float>) |
| 61 | Info | Unity Log | 30345-34730 | Local client hit enemy Bulbmin_irWwW #<int> with force of 9999. |
| 61 | Info | LethalMin | 30346-34731 | Bulbmin_irWwW: Has Invincible mode when hit |
| 61 | Info | Unity Log | 30347-34732 | [Lethal Doors Fixed] Bulbmin_axAI8RJ is in danger zone at position (<float>, <float>, <float>) |
| 61 | Info | Unity Log | 30348-34733 | Local client hit enemy Bulbmin_axAI8RJ #<int> with force of 9999. |
| 61 | Info | LethalMin | 30349-34734 | Bulbmin_axAI8RJ: Has Invincible mode when hit |
| 61 | Info | Unity Log | 33250-34735 | [Lethal Doors Fixed] White Pikmin_3SEYVg is in danger zone at position (<float>, <float>, <float>) |
| 61 | Info | Unity Log | 33251-34736 | Local client hit enemy White Pikmin_3SEYVg #<int> with force of 9999. |
| 61 | Info | LethalMin | 33252-34737 | White Pikmin_3SEYVg: Has Invincible mode when hit |
| 60 | Debug | LethalMin | 14226-27840 | <ID Not Set>: Setting collision mode to <int> |
| 58 | Debug | LethalMin | 28104-29606 | Chosen Route Strategy: DirectOutdoorStrategy (Priority <int>)  ↩ (ToShip) Route Context: IsInside=False, IsInShip=False, CurrentFloor=null, DestinationIsInside=False, DestinationIsInShip=True |
| 58 | Debug | LethalMin | 28106-29607 | Generated Route Nodes: Ship |
| 54 | Debug | LethalMin | 27943-29496 | Cannot do throw while not holding a pikmin |
| 52 | Debug | Jetpack Fixes | 849-3670 | Transpiler: Replace "Gravity" with "Inertia" |
| 52 | Debug | ReXuvination | 8784-25993 | Optimised Collider layers in InteractTrigger for Object: Cube (<int>) (UnityEngine.GameObject) |
| 52 | Info | Unity Log | 14673-55239 | Interact trigger destroying! name: Cube (<int>) |
| 48 | Debug | LethalMin | 8764-22786 | PikminNoticeZone has spawned |
| 48 | Warning | Unity Log | 11450-23476 | Failed to create agent because there is no valid NavMesh |
| 45 | Info | ReservedItemSlotCore-2.0.41 | 11448-23475 | Initializing ReservedPlayerData for player: Player (<int>) |
| 42 | Warning | Unity Log | 3771-4001 | The referenced script on this Behaviour (Game Object 'CreeperVine (<int>)') is missing! |
| 41 | Info | Unity Log | 12450-35065 | Anomaly random yrotation farthest: <int> |
| 38 | Info | Unity Log | 8692-55196 | DropAllHeldItems; player pos: (<float>, <float>, <float>) |
| 38 | Info | Unity Log | 29991-31381 | [Lethal Doors Fixed] Purple Pikmin_OcBGak3 is in danger zone at position (<float>, <float>, <float>) |
| 38 | Info | Unity Log | 29992-31382 | Local client hit enemy Purple Pikmin_OcBGak3 #<int> with force of 9999. |
| 38 | Info | LethalMin | 29993-31383 | Purple Pikmin_OcBGak3: Has Invincible mode when hit |
| 38 | Info | Unity Log | 29994-31390 | [Lethal Doors Fixed] Purple Pikmin_UHnG is in danger zone at position (<float>, <float>, <float>) |
| 38 | Info | Unity Log | 29995-31391 | Local client hit enemy Purple Pikmin_UHnG #<int> with force of 9999. |
| 38 | Info | LethalMin | 29996-31392 | Purple Pikmin_UHnG: Has Invincible mode when hit |
| 36 | Info | Unity Log | 8691-22764 | DropAllHeldItems called on player 'Player #<int>'; itemsFall: False; disconnecting: False; ItemSlots length: <int>; isHoldingObject: False |
| 36 | Info | LethalMin | 28259-28960 | AnvilPrefab(Clone) has cleared its route |
| 35 | Warning | LethalMin | 28258-28845 | AnvilPrefab(Clone) route has been invalidated (NodeBecameUnreachable), clearing route |
| 34 | Message | LethalMin | 14224-27598 | Spawning: Purple Pikmin |
| 34 | Debug | LethalMin | 14227-27601 | Purple Pikmin: No sound pack found for generation Pikmin4, using default sound pack. |
| 34 | Warning | Unity Log | 14252-27609 | PurplePikmin4 Pik Animation State '' not found |
| 32 | Warning | Unity Log | 11547-55208 | Parent of RectTransform is being set with parent property. Consider using the SetParent method instead, with the worldPositionStays argument set to false. This will retain local orientation and scale rather than world orientation and sca... |
| 31 | Debug | LethalMin | 14212-27467 | OnionHUDSlot: DownPressed: (x1) Purple Pikmin (IO:<int>) (EC:<int>) (PIC:<int>) (PIF:<int>) |
| 30 | Debug | LethalMin | 14225-27599 | <ID Not Set>: Is linking onto Link |
| 30 | Debug | LethalMin | 18857-27638 | OnionHUDSlot: DownPressed: (x1) Yellow Pikmin (IO:<int>) (EC:<int>) (PIC:<int>) (PIF:<int>) |
| 30 | Message | LethalMin | 18875-27838 | Spawning: Yellow Pikmin |
| 30 | Debug | LethalMin | 18878-27841 | Yellow Pikmin: No sound pack found for generation Pikmin4, using default sound pack. |
| 30 | Warning | Unity Log | 18903-27849 | YellowPikmin4 Pik Animation State '' not found |
| 30 | Info | Unity Log | 30105-31414 | [Lethal Doors Fixed] Yellow Pikmin_2nE2lyy is in danger zone at position (<float>, <float>, <float>) |
| 30 | Info | Unity Log | 30106-31415 | Local client hit enemy Yellow Pikmin_2nE2lyy #<int> with force of 9999. |
| 30 | Info | LethalMin | 30107-31416 | Yellow Pikmin_2nE2lyy: Has Invincible mode when hit |
| 30 | Info | LethalMin | 49745-55073 | data moon: <int>, current moon: <int> |
| 28 | Debug | LethalMin | 11814-26038 | Initializing PikminItem Key(Clone) with item Key(Clone) (True) |
| 27 | Debug | Spawn Cycle Fixes | 12668-25705 | Predictor: Spawn wave at time <int> |
| 27 | Debug | Spawn Cycle Fixes | 12669-25706 | Predictor: Base amount is <float> |
| 27 | Debug | Spawn Cycle Fixes | 12670-25707 | Predictor: Adjusted amount is <float> (<int> days left) |
| 27 | Debug | Spawn Cycle Fixes | 12671-25708 | Predictor: Spawning <int> enemies |
