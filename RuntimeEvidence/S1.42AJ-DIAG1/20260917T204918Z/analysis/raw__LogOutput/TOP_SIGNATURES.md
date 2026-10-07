# Top normalized runtime signatures

Every log event was processed. Dynamic GUID/hex/numeric values are normalized for aggregation.
Full normalized signature coverage is stored in `signatures/` and indexed by `SIGNATURES_MANIFEST.json`.

| Count | Level | Source | Lines | Normalized event |
|---:|---|---|---:|---|
| 511 | Info | Unity Log | 16417-18616 | enemy rush index is <int>; current index <int> |
| 393 | Error | Unity Log | 12888-13770 | RuntimeNavMeshBuilder: Source mesh Cube is skipped because it does not allow read access |
| 306 | Warning | Coroner | 12131-18629 | Could not access dying player: Collider was not a player! |
| 306 | Warning | Coroner | 12132-18630 | Could not access dying player: Index not assigned! |
| 306 | Debug | Coroner | 12133-18631 | Handling Out of Bounds death... |
| 250 | Debug | TestAccountCore | 12625-12874 | Hazard injection: <int> matches, <int> hazards |
| 170 | Error | Unity Log | 12880-13773 | RuntimeNavMeshBuilder: Source mesh Cube.002 is skipped because it does not allow read access |
| 162 | Error | Unity Log | 12881-13774 | RuntimeNavMeshBuilder: Source mesh Terminal.003 is skipped because it does not allow read access |
| 150 | Error | Unity Log | 12878-13775 | RuntimeNavMeshBuilder: Source mesh office_table_01 is skipped because it does not allow read access |
| 137 | Warning | Unity Log | 3735-4034 | The referenced script (UnityMeshSimplifier.LODBackupComponent) on this Behaviour is missing! |
| 101 | Debug | LethalMin | 16534-16758 | Yellow Pikmin_LuMKh: Hitting enemy with: <float> |
| 95 | Warning | Unity Log | 2182-4080 | The referenced script on this Behaviour (Game Object '') is missing! |
| 92 | Debug | LethalMin | 14450-18719 | Sprout Setting growth stage to <int> |
| 87 | Warning | ainavt.lc.lethalconfig | 8279-8365 | Mod for assembly not found. |
| 86 | Info | ImmersiveScrap | 4243-4498 | Registered spawn rate for Vanilla to <int> |
| 86 | Info | ImmersiveScrap | 4244-4499 | Registered spawn rate for Custom to <int> |
| 70 | Debug | ReXuvination | 8793-14663 | Optimised Collider layers in InteractTrigger for Object: Cube (UnityEngine.GameObject) |
| 70 | Info | Unity Log | 18983-19228 | Interact trigger destroying! name: Cube |
| 64 | Debug | ReXuvination | 13799-13863 | Optimised Collider layers in DoorLock for Object: Cube (UnityEngine.GameObject) |
| 52 | Debug | Jetpack Fixes | 849-3674 | Transpiler: Replace "Gravity" with "Inertia" |
| 50 | Debug | GeneralImprovements | 8830-18732 | Updated time display. |
| 49 | Debug | ReXuvination | 11735-14710 | Optimised Collider layers in InteractTrigger for Object: InteractTrigger (UnityEngine.GameObject) |
| 49 | Info | Unity Log | 13795-19177 | Interact trigger destroying! name: InteractTrigger |
| 48 | Info | Unity Log | 8698-8767 | Item slot #<int> null?: True |
| 42 | Warning | Unity Log | 3776-4006 | The referenced script on this Behaviour (Game Object 'CreeperVine (<int>)') is missing! |
| 41 | Info | Unity Log | 10971-11131 | item awake: ChangableSuit(Clone); id: <int> |
| 41 | Warning | Unity Log | 10972-11132 | NetworkVariable is written to, but doesn't know its NetworkBehaviour yet. Are you modifying a NetworkVariable before the NetworkObject is spawned? |
| 41 | Debug | ScienceBirdTweaks | 10973-11133 | Parenting suits to ship! |
| 41 | Debug | ReXuvination | 11737-11777 | Optimised Collider layers in InteractTrigger for Object: ChangableSuit(Clone) (UnityEngine.GameObject) |
| 41 | Info | Unity Log | 19094-19174 | Interact trigger destroying! name: ChangableSuit(Clone) |
| 39 | Warning | Unity Log | 14941-16874 | PlayOneShot was called with a null AudioClip. |
| 36 | Warning | Unity Log | 15977-18238 | Failed to create agent because it is not close enough to the NavMesh |
| 34 | Warning | Unity Log | 12434-12573 | BoxCollider does not support negative scale or size. ↩ The effective box size has been forced positive and is likely to give unexpected collision geometry. ↩ If you absolutely need to use negative scaling you can use the convex MeshColli... |
| 32 | Info | Unity Log | 10918-10949 | Item sales percentages #<int>: <int> |
| 30 | Info | Unity Log | 16476-18617 | Hours: <int> ; Time: <float> \| Enemy #<int> 'kamikazieBugs' : probability: <int> |
| 23 | Debug | Coroner | 12183-18714 | Querying target player parameters pre-death... |
| 23 | Debug | Coroner | 12184-18715 | Query successful!True |
| 23 | Warning | Unity Log | 17965-18644 | [Netcode] NetworkObject #<int> moved to the root because its parent NetworkObject #<int> is destroyed |
| 22 | Debug | LethalMin | 15953-16308 | <ID Not Set>: Setting collision mode to <int> |
| 20 | Warning | Unity Log | 3847-4005 | The referenced script on this Behaviour (Game Object 'BushyBuish') is missing! |
| 18 | Warning | Unity Log | 2055-2072 | LethalLevelLoader.ExtendedItem must be instantiated using the ScriptableObject.CreateInstance method instead of new ExtendedItem. |
| 18 | Warning | Unity Log | 4215-4233 | The referenced script on this Behaviour (Game Object '<null>') is missing! |
| 16 | Debug | DawnLib | 518-2382 | transpiling Terminal::TextPostProcess with UseFailedNameResults. instructions: <int> |
| 16 | Debug | LethalMin | 8769-8786 | PikminNoticeZone has spawned |
| 16 | Warning | Unity Log | 11472-11732 | Failed to create agent because there is no valid NavMesh |
| 16 | Debug | Coroner | 12220-12235 | Clearing cause of death for player <int> |
| 16 | Debug | Spawn Cycle Fixes | 14152-14418 | Predictor: Processing "KamikazieBug" |
| 16 | Debug | Spawn Cycle Fixes | 14153-14419 | Predictor: "KamikazieBug" at <int> weight (<int> spawned) |
| 16 | Info | Unity Log | 16438-18589 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Stingray' : probability: <int> |
| 16 | Debug | LethalMin | 16848-17765 | Chosen Route Strategy: DirectOutdoorStrategy (Priority <int>)  ↩ (ToShip) Route Context: IsInside=False, IsInShip=False, CurrentFloor=null, DestinationIsInside=False, DestinationIsInShip=True |
| 16 | Debug | LethalMin | 16850-17766 | Generated Route Nodes: Ship |
| 15 | Info | ReservedItemSlotCore-2.0.41 | 11470-11731 | Initializing ReservedPlayerData for player: Player (<int>) |
| 15 | Message | LethalMin | 14581-16218 | Spawning: Purple Pikmin |
| 15 | Debug | LethalMin | 14751-16221 | Purple Pikmin: No sound pack found for generation Pikmin4, using default sound pack. |
| 15 | Warning | Unity Log | 14772-16229 | PurplePikmin4 Pik Animation State '' not found |
| 15 | Debug | LethalMin | 15939-16247 | OnionHUDSlot: DownPressed: (x1) Yellow Pikmin (IO:<int>) (EC:<int>) (PIC:<int>) (PIF:<int>) |
| 15 | Message | LethalMin | 15951-16306 | Spawning: Yellow Pikmin |
| 15 | Debug | LethalMin | 15954-16309 | Yellow Pikmin: No sound pack found for generation Pikmin4, using default sound pack. |
| 15 | Warning | Unity Log | 15979-16317 | YellowPikmin4 Pik Animation State '' not found |
| 15 | Info | Unity Log | 16418-18579 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Centipede' : probability: <int> |
| 15 | Info | Unity Log | 16422-18581 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Hoarding bug' : probability: <int> |
| 15 | Info | Unity Log | 16428-18583 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Blob' : probability: <int> |
| 15 | Info | Unity Log | 16432-18585 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Puffer' : probability: <int> |
| 15 | Info | Unity Log | 16434-18587 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Nutcracker' : probability: <int> |
| 15 | Info | Unity Log | 16440-18591 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Masked' : probability: <int> |
| 15 | Info | Unity Log | 16446-18593 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Clay Surgeon' : probability: <int> |
| 15 | Info | Unity Log | 16454-18595 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Locker' : probability: <int> |
| 15 | Info | Unity Log | 16456-18597 | Hours: <int> ; Time: <float> \| Enemy #<int> 'ImmortalSnail' : probability: <int> |
| 15 | Info | Unity Log | 16458-18599 | Hours: <int> ; Time: <float> \| Enemy #<int> 'HarpGhost' : probability: <int> |
| 15 | Info | Unity Log | 16460-18601 | Hours: <int> ; Time: <float> \| Enemy #<int> 'BagpipeGhost' : probability: <int> |
| 15 | Info | Unity Log | 16468-18603 | Hours: <int> ; Time: <float> \| Enemy #<int> 'SlendermanEnemy' : probability: <int> |
| 15 | Info | Unity Log | 16470-18605 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Cabinet' : probability: <int> |
| 15 | Info | Unity Log | 16474-18607 | Hours: <int> ; Time: <float> \| Enemy #<int> 'RollingGiant' : probability: <int> |
| 15 | Info | Unity Log | 16478-18611 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Boomba' : probability: <int> |
| 15 | Info | Unity Log | 16486-18613 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Janitor' : probability: <int> |
| 15 | Info | Unity Log | 16494-18615 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Transporter' : probability: <int> |
| 14 | Debug | ReXuvination | 8789-14670 | Optimised Collider layers in InteractTrigger for Object: Cube (<int>) (UnityEngine.GameObject) |
| 14 | Debug | LightsOut | 11147-11174 | PhysicsProp has no light |
| 14 | Info | Unity Log | 16659-18725 | Spawned enemy from vent |
| 14 | Debug | LethalMin | 18025-18038 | OnionHUDSlot: UpPressed: (x1) Yellow Pikmin (IS:<int>) (EC:<int>) (PIC:<int>) |
| 14 | Info | Unity Log | 18984-19232 | Interact trigger destroying! name: Cube (<int>) |
| 13 | Info | LethalPerformance.Patcher | 4638-16663 | Saved <int> config(s) |
| 13 | Debug | LethalMin | 16409-17803 | Bulbmin_bkWk: Setting collision mode to <int> |
| 13 | Info | Unity Log | 16430-18524 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Spring' : probability: <int> |
| 13 | Info | Unity Log | 16444-18534 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Butler' : probability: <int> |
| 13 | Info | Unity Log | 16448-18538 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Girl' : probability: <int> |
| 13 | Info | Unity Log | 16450-18540 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Football' : probability: <int> |
| 13 | Info | Unity Log | 16452-18542 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Herobrine' : probability: <int> |
| 13 | Info | Unity Log | 16482-18562 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Peace Keeper' : probability: <int> |
| 13 | Info | Unity Log | 16484-18564 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Lord Of The Manor' : probability: <int> |
| 13 | Info | Unity Log | 16490-18568 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Mistress' : probability: <int> |
| 13 | Info | Unity Log | 16492-18570 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Duck' : probability: <int> |
| 12 | Debug | GeneralImprovements | 685-2004 | Patching Terminal.ParsePlayerSentence to set dropship item limit to 24. |
| 12 | Debug | Buttery Fixes | 750-3642 | Transpiler (RoundManager.GenerateNewLevelClientRpc): Cache mold manager |
| 12 | Debug | Coroner | 936-2377 | Injecting patch #<int> into Landmine.SpawnExplosion... |
| 12 | Debug | Coroner | 937-2378 | Success. |
| 12 | Info | Unity Log | 8696-8762 | DropAllHeldItems called on player 'Player #<int>'; itemsFall: False; disconnecting: False; ItemSlots length: <int>; isHoldingObject: False |
| 12 | Info | Unity Log | 8697-8763 | DropAllHeldItems; player pos: (<float>, <float>, <float>) |
| 12 | Info | Unity Log | 16488-18458 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Nancy' : probability: <int> |
| 11 | Debug | PizzaTowerEscapeMusic GameEventListener | 12140-18664 | Player entered ship |
