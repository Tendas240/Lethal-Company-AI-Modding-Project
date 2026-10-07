# Top normalized runtime signatures

Every log event was processed. Dynamic GUID/hex/numeric values are normalized for aggregation.
Full normalized signature coverage is stored in `signatures/` and indexed by `SIGNATURES_MANIFEST.json`.

| Count | Level | Source | Lines | Normalized event |
|---:|---|---|---:|---|
| 934 | Warning | Unity Log | 14887-19224 | PlayOneShot was called with a null AudioClip. |
| 443 | Info | Unity Log | 15704-17325 | enemy rush index is <int>; current index <int> |
| 319 | Warning | Coroner | 11475-17770 | Could not access dying player: Collider was not a player! |
| 319 | Warning | Coroner | 11476-17771 | Could not access dying player: Index not assigned! |
| 319 | Debug | Coroner | 11477-17772 | Handling Out of Bounds death... |
| 238 | Debug | TestAccountCore | 12360-12597 | Hazard injection: <int> matches, <int> hazards |
| 223 | Debug | ReXuvination | 12091-12338 | Optimised Collider layers in InteractTrigger for Object: Tele in Trigger (UnityEngine.GameObject) |
| 223 | Info | Unity Log | 12602-19758 | Interact trigger destroying! name: Tele in Trigger |
| 145 | Debug | GeneralImprovements | 8539-17765 | Updated time display. |
| 144 | Debug | Coroner | 18670-19206 | Post step action done: CauseOfDeathPatchState(<int>:True, False==false?) |
| 142 | Warning | Coroner | 18917-19205 | Could not access dying player: Player already had a precise cause of death! |
| 137 | Warning | Unity Log | 3502-3824 | The referenced script (UnityMeshSimplifier.LODBackupComponent) on this Behaviour is missing! |
| 126 | Debug | LethalMin | 13575-18932 | Sprout Setting growth stage to <int> |
| 87 | Warning | ainavt.lc.lethalconfig | 7988-8074 | Mod for assembly not found. |
| 86 | Info | ImmersiveScrap | 4011-4266 | Registered spawn rate for Vanilla to <int> |
| 86 | Info | ImmersiveScrap | 4012-4267 | Registered spawn rate for Custom to <int> |
| 86 | Debug | Coroner | 11878-18668 | Querying target player parameters pre-death... |
| 86 | Debug | Coroner | 11879-18669 | Query successful!True |
| 83 | Warning | Unity Log | 3479-3848 | The referenced script on this Behaviour (Game Object '') is missing! |
| 56 | Info | Unity Log | 12922-18901 | Anomaly random yrotation farthest: <int> |
| 55 | Info | Unity Log | 8407-18725 | Item slot #<int> null?: True |
| 54 | Debug | ReXuvination | 8507-13122 | Optimised Collider layers in InteractTrigger for Object: Trigger (UnityEngine.GameObject) |
| 54 | Info | Unity Log | 13250-19750 | Interact trigger destroying! name: Trigger |
| 52 | Debug | Jetpack Fixes | 795-3441 | Transpiler: Replace "Gravity" with "Inertia" |
| 51 | Debug | ReXuvination | 11483-13828 | Optimised Collider layers in InteractTrigger for Object: InteractTrigger (UnityEngine.GameObject) |
| 51 | Info | Unity Log | 12939-19712 | Interact trigger destroying! name: InteractTrigger |
| 45 | Debug | ReXuvination | 13014-13121 | Optimised Collider layers in InteractTrigger for Object: Trigger (close) (UnityEngine.GameObject) |
| 45 | Info | Unity Log | 19499-19605 | Interact trigger destroying! name: Trigger (close) |
| 42 | Warning | Unity Log | 3545-3775 | The referenced script on this Behaviour (Game Object 'CreeperVine (<int>)') is missing! |
| 42 | Error | Unity Log | 12824-12921 | RuntimeNavMeshBuilder: Source mesh CardboardBox is skipped because it does not allow read access |
| 41 | Info | Unity Log | 10674-10834 | item awake: ChangableSuit(Clone); id: <int> |
| 41 | Warning | Unity Log | 10675-10835 | NetworkVariable is written to, but doesn't know its NetworkBehaviour yet. Are you modifying a NetworkVariable before the NetworkObject is spawned? |
| 41 | Debug | ScienceBirdTweaks | 10676-10836 | Parenting suits to ship! |
| 41 | Debug | ReXuvination | 11486-11526 | Optimised Collider layers in InteractTrigger for Object: ChangableSuit(Clone) (UnityEngine.GameObject) |
| 41 | Info | Unity Log | 19629-19709 | Interact trigger destroying! name: ChangableSuit(Clone) |
| 40 | Warning | Unity Log | 17433-18657 | Only custom filters can be played. Please add a custom filter or an audioclip to the audiosource (SweepingSFX). |
| 32 | Info | Unity Log | 10621-10652 | Item sales percentages #<int>: <int> |
| 29 | Debug | ReXuvination | 8502-13083 | Optimised Collider layers in InteractTrigger for Object: Cube (UnityEngine.GameObject) |
| 29 | Debug | Coroner | 17926-18048 | Handling Baboon Hawk damage... |
| 29 | Warning | Coroner | 17927-18049 | Could not access dying player: Player is still alive! |
| 29 | Info | Unity Log | 19535-19742 | Interact trigger destroying! name: Cube |
| 26 | Debug | Starlancer AI Fix | 13843-15327 | Pikmin(Clone) spawned inside; Switching to interior AI. Setting Favorite Spot to ainode (UnityEngine.Transform). |
| 25 | Debug | ReXuvination | 12943-12967 | Optimised Collider layers in DoorLock for Object: Cube (UnityEngine.GameObject) |
| 22 | Debug | LethalMin | 14955-15184 | OnionHUDSlot: DownPressed: (x1) Yellow Pikmin (IO:<int>) (EC:<int>) (PIC:<int>) (PIF:<int>) |
| 20 | Warning | Unity Log | 3616-3774 | The referenced script on this Behaviour (Game Object 'BushyBuish') is missing! |
| 20 | Message | LethalMin | 14973-15324 | Spawning: Yellow Pikmin |
| 20 | Debug | LethalMin | 14975-15326 | <ID Not Set>: Setting collision mode to <int> |
| 20 | Debug | LethalMin | 14977-15328 | Yellow Pikmin: No sound pack found for generation Pikmin4, using default sound pack. |
| 20 | Warning | Unity Log | 15000-15334 | Failed to create agent because it is not close enough to the NavMesh |
| 20 | Warning | Unity Log | 15002-15336 | YellowPikmin4 Pik Animation State '' not found |
| 19 | Error | Unity Log | 12860-12909 | RuntimeNavMeshBuilder: Source mesh LargerPillow is skipped because it does not allow read access |
| 18 | Warning | Unity Log | 1988-2005 | LethalLevelLoader.ExtendedItem must be instantiated using the ScriptableObject.CreateInstance method instead of new ExtendedItem. |
| 18 | Warning | Unity Log | 3983-4001 | The referenced script on this Behaviour (Game Object '<null>') is missing! |
| 16 | Debug | DawnLib | 465-2177 | transpiling Terminal::TextPostProcess with UseFailedNameResults. instructions: <int> |
| 16 | Debug | LethalMin | 8478-8495 | PikminNoticeZone has spawned |
| 16 | Warning | Unity Log | 11175-11435 | Failed to create agent because there is no valid NavMesh |
| 16 | Debug | Coroner | 11915-11930 | Clearing cause of death for player <int> |
| 15 | Info | ReservedItemSlotCore-2.0.41 | 11173-11434 | Initializing ReservedPlayerData for player: Player (<int>) |
| 14 | Debug | LightsOut | 10850-10877 | PhysicsProp has no light |
| 14 | Debug | LethalMin | 18172-18260 | Yellow Pikmin_hcRGph: Hitting enemy with: <float> |
| 13 | Info | Unity Log | 8406-18688 | DropAllHeldItems; player pos: (<float>, <float>, <float>) |
| 13 | Debug | PizzaTowerEscapeMusic GameEventListener | 11841-17723 | Player entered ship |
| 13 | Debug | LethalMin | 13586-13703 | Spawning sprout <int> iteration(<int>) at: [(<float>, <float>, <float>), (<float>, <float>, <float>)] With type: Winged Pikmin odds:(<float>) rng: (<float> / <float>) |
| 13 | Debug | LethalMin | 13588-13705 | Winged Pikmin sprout initalized at ((<float>, <float>, <float>),(<float>, <float>, <float>)) |
| 13 | Debug | PizzaTowerEscapeMusic GameEventListener | 14891-17764 | Player exited ship |
| 13 | Debug | LethalMin | 15197-18835 | Yellow Pikmin_3wnH: Setting collision mode to <int> |
| 13 | Info | Unity Log | 15705-17292 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Centipede' : probability: <int> |
| 13 | Info | Unity Log | 15709-17294 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Hoarding bug' : probability: <int> |
| 13 | Info | Unity Log | 15717-17296 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Puffer' : probability: <int> |
| 13 | Info | Unity Log | 15719-17298 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Nutcracker' : probability: <int> |
| 13 | Info | Unity Log | 15723-17300 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Stingray' : probability: <int> |
| 13 | Info | Unity Log | 15725-17302 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Masked' : probability: <int> |
| 13 | Info | Unity Log | 15731-17304 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Clay Surgeon' : probability: <int> |
| 13 | Info | Unity Log | 15739-17306 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Locker' : probability: <int> |
| 13 | Info | Unity Log | 15741-17308 | Hours: <int> ; Time: <float> \| Enemy #<int> 'ImmortalSnail' : probability: <int> |
| 13 | Info | Unity Log | 15743-17310 | Hours: <int> ; Time: <float> \| Enemy #<int> 'HarpGhost' : probability: <int> |
| 13 | Info | Unity Log | 15745-17312 | Hours: <int> ; Time: <float> \| Enemy #<int> 'BagpipeGhost' : probability: <int> |
| 13 | Info | Unity Log | 15753-17314 | Hours: <int> ; Time: <float> \| Enemy #<int> 'SlendermanEnemy' : probability: <int> |
| 13 | Info | Unity Log | 15755-17316 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Cabinet' : probability: <int> |
| 13 | Info | Unity Log | 15759-17318 | Hours: <int> ; Time: <float> \| Enemy #<int> 'RollingGiant' : probability: <int> |
| 13 | Info | Unity Log | 15761-17320 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Boomba' : probability: <int> |
| 13 | Info | Unity Log | 15769-17322 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Janitor' : probability: <int> |
| 13 | Info | Unity Log | 15771-17324 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Nancy' : probability: <int> |
| 13 | Info | Unity Log | 15777-17326 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Transporter' : probability: <int> |
| 13 | Info | Unity Log | 15965-17554 | Spawned enemy from vent |
| 12 | Debug | GeneralImprovements | 631-1937 | Patching Terminal.ParsePlayerSentence to set dropship item limit to 24. |
| 12 | Debug | Buttery Fixes | 696-3409 | Transpiler (RoundManager.GenerateNewLevelClientRpc): Cache mold manager |
| 12 | Debug | Coroner | 882-2172 | Injecting patch #<int> into Landmine.SpawnExplosion... |
| 12 | Debug | Coroner | 883-2173 | Success. |
| 12 | Info | Unity Log | 8405-8471 | DropAllHeldItems called on player 'Player #<int>'; itemsFall: False; disconnecting: False; ItemSlots length: <int>; isHoldingObject: False |
| 12 | Warning | Unity Log | 11272-18736 | Parent of RectTransform is being set with parent property. Consider using the SetParent method instead, with the worldPositionStays argument set to false. This will retain local orientation and scale rather than world orientation and sca... |
| 12 | Debug | LethalMin | 15014-18781 | Yellow Pikmin_G5l3h: Setting collision mode to <int> |
| 12 | Debug | LethalMin | 15104-18817 | Yellow Pikmin_XYErHj: Setting collision mode to <int> |
| 12 | Debug | LethalMin | 15257-18859 | Yellow Pikmin_IkVZWQe: Setting collision mode to <int> |
| 12 | Info | Unity Log | 15707-17223 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Bunker Spider' : probability: <int> |
| 12 | Info | Unity Log | 15711-17227 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Flowerman' : probability: <int> |
| 12 | Info | Unity Log | 15713-17229 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Crawler' : probability: <int> |
| 12 | Info | Unity Log | 15721-17235 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Maneater' : probability: <int> |
| 12 | Info | Unity Log | 15727-17241 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Jester' : probability: <int> |
| 12 | Info | Unity Log | 15729-17243 | Hours: <int> ; Time: <float> \| Enemy #<int> 'Butler' : probability: <int> |
