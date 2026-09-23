# Top normalized runtime signatures

Every log event was processed. Dynamic GUID/hex/numeric values are normalized for aggregation.
Full normalized signature coverage is stored in `signatures/` and indexed by `SIGNATURES_MANIFEST.json`.

| Count | Level | Source | Lines | Normalized event |
|---:|---|---|---:|---|
| 700 | Debug | TestAccountCore | 12874-13573 | Hazard injection: <int> matches, <int> hazards |
| 552 | Debug | Coroner | 12020-16925 | Handling Out of Bounds death... |
| 529 | Warning | Coroner | 12019-16924 | Could not access dying player: Index not assigned! |
| 528 | Warning | Coroner | 12018-16923 | Could not access dying player: Collider was not a player! |
| 374 | Error | Unity Log | 13576-14037 | RuntimeNavMeshBuilder: Source mesh Cube.002 is skipped because it does not allow read access |
| 137 | Warning | Unity Log | 3732-4024 | The referenced script (UnityMeshSimplifier.LODBackupComponent) on this Behaviour is missing! |
| 95 | Warning | Unity Log | 2182-4079 | The referenced script on this Behaviour (Game Object '') is missing! |
| 86 | Info | ImmersiveScrap | 4242-4497 | Registered spawn rate for Vanilla to <int> |
| 86 | Info | ImmersiveScrap | 4243-4498 | Registered spawn rate for Custom to <int> |
| 86 | Warning | ainavt.lc.lethalconfig | 8277-8362 | Mod for assembly not found. |
| 70 | Info | Unity Log | 16933-17329 | enemy rush index is <int>; current index <int> |
| 52 | Debug | Jetpack Fixes | 849-3673 | Transpiler: Replace "Gravity" with "Inertia" |
| 48 | Info | Unity Log | 8695-8764 | Item slot #<int> null?: True |
| 44 | Error | Unity Log | 13634-14041 | RuntimeNavMeshBuilder: Source mesh Cube is skipped because it does not allow read access |
| 42 | Warning | Unity Log | 3775-4005 | The referenced script on this Behaviour (Game Object 'CreeperVine (<int>)') is missing! |
| 42 | Warning | Unity Log | 12511-12870 | BoxCollider does not support negative scale or size. ↩ The effective box size has been forced positive and is likely to give unexpected collision geometry. ↩ If you absolutely need to use negative scaling you can use the convex MeshColli... |
| 42 | Error | Unity Log | 13636-13902 | RuntimeNavMeshBuilder: Source mesh Cylinder.002 is skipped because it does not allow read access |
| 41 | Info | Unity Log | 10967-11127 | item awake: ChangableSuit(Clone); id: <int> |
| 41 | Warning | Unity Log | 10968-11128 | NetworkVariable is written to, but doesn't know its NetworkBehaviour yet. Are you modifying a NetworkVariable before the NetworkObject is spawned? |
| 41 | Debug | ScienceBirdTweaks | 10969-11129 | Parenting suits to ship! |
| 41 | Debug | ReXuvination | 11715-11755 | Optimised Collider layers in InteractTrigger for Object: ChangableSuit(Clone) (UnityEngine.GameObject) |
| 41 | Debug | Coroner | 12075-17456 | Querying target player parameters pre-death... |
| 41 | Debug | Coroner | 12076-17457 | Query successful!True |
| 41 | Info | Unity Log | 17730-17810 | Interact trigger destroying! name: ChangableSuit(Clone) |
| 38 | Debug | Spawn Cycle Fixes | 14401-14755 | Predictor: Processing "DocileLocustBees" |
| 33 | Error | Unity Log | 12214-12246 | Can't remove MeshCollider because DawnSurface (Script) depends on it |
| 32 | Info | Unity Log | 10914-10945 | Item sales percentages #<int>: <int> |
| 25 | Info | BrutalCompanyMinusExtraReborn | 12403-12432 | Time:<float> + $Value:<float> |
| 24 | Warning | Unity Log | 12541-12837 | BoxCollider does not support negative scale or size. ↩ The effective box size has been forced positive and is likely to give unexpected collision geometry. ↩ If you absolutely need to use negative scaling you can use the convex MeshColli... |
| 22 | Info | Unity Log | 14253-14274 | BigDoorStore(Clone) creating doorcode object in parent MapScreenUIWorldSpace (UnityEngine.RectTransform): DoorCodeUIObject(Clone) |
| 21 | Error | Unity Log | 12247-12267 | Can't remove BoxCollider because DawnSurface (Script) depends on it |
| 21 | Debug | Starlancer AI Fix | 15085-15369 | Pikmin(Clone) spawned inside; Switching to interior AI. Setting Favorite Spot to AInode (<int>) (UnityEngine.Transform). |
| 20 | Warning | Unity Log | 3846-4004 | The referenced script on this Behaviour (Game Object 'BushyBuish') is missing! |
| 19 | Debug | Spawn Cycle Fixes | 14395-14741 | Predictor: Processing "BaboonHawk" |
| 19 | Debug | Spawn Cycle Fixes | 14397-14742 | Predictor: Processing "MouthDog" |
| 19 | Debug | Spawn Cycle Fixes | 14399-14743 | Predictor: Processing "Vermin" |
| 19 | Debug | Spawn Cycle Fixes | 14400-14744 | Predictor: "Vermin" at <int> weight (<int> spawned) |
| 19 | Debug | Spawn Cycle Fixes | 14403-14746 | Predictor: Processing "JPOGRaptor" |
| 19 | Debug | Spawn Cycle Fixes | 14404-14747 | Predictor: Processing "JPOGTrexObj" |
| 19 | Debug | Spawn Cycle Fixes | 14405-14748 | Predictor: Processing "CactusBudlingObj" |
| 19 | Debug | Spawn Cycle Fixes | 14407-14749 | Predictor: Processing "DriftwoodMenaceObj" |
| 19 | Debug | Spawn Cycle Fixes | 14409-14750 | Predictor: Processing "MonarchObj" |
| 19 | Debug | Spawn Cycle Fixes | 14411-14751 | Predictor: Processing "RedwoodTitanObj" |
| 19 | Debug | Spawn Cycle Fixes | 14413-14752 | Predictor: Processing "DebtCollectorObj" |
| 19 | Debug | Spawn Cycle Fixes | 14414-14753 | Predictor: Processing "GuardsmanObj" |
| 19 | Debug | Spawn Cycle Fixes | 14415-14754 | Predictor: "GuardsmanObj" at <int> weight (<int> spawned) |
| 19 | Debug | Spawn Cycle Fixes | 14418-14756 | Predictor: <int> total weight |
| 18 | Warning | Unity Log | 2055-2072 | LethalLevelLoader.ExtendedItem must be instantiated using the ScriptableObject.CreateInstance method instead of new ExtendedItem. |
| 18 | Warning | Unity Log | 4214-4232 | The referenced script on this Behaviour (Game Object '<null>') is missing! |
| 18 | Warning | Unity Log | 12484-12750 | BoxCollider does not support negative scale or size. ↩ The effective box size has been forced positive and is likely to give unexpected collision geometry. ↩ If you absolutely need to use negative scaling you can use the convex MeshColli... |
| 18 | Warning | Unity Log | 12508-12873 | BoxCollider does not support negative scale or size. ↩ The effective box size has been forced positive and is likely to give unexpected collision geometry. ↩ If you absolutely need to use negative scaling you can use the convex MeshColli... |
| 17 | Debug | LethalMin | 14779-17240 | Sprout Setting growth stage to <int> |
| 16 | Debug | DawnLib | 518-2382 | transpiling Terminal::TextPostProcess with UseFailedNameResults. instructions: <int> |
| 16 | Debug | LethalMin | 8766-8783 | PikminNoticeZone has spawned |
| 16 | Warning | Unity Log | 11450-11710 | Failed to create agent because there is no valid NavMesh |
| 16 | Debug | ReXuvination | 11713-15072 | Optimised Collider layers in InteractTrigger for Object: InteractTrigger (UnityEngine.GameObject) |
| 16 | Debug | Coroner | 12170-12185 | Clearing cause of death for player <int> |
| 16 | Info | Unity Log | 17675-17813 | Interact trigger destroying! name: InteractTrigger |
| 15 | Info | ReservedItemSlotCore-2.0.41 | 11448-11709 | Initializing ReservedPlayerData for player: Player (<int>) |
| 14 | Message | LethalMin | 14837-14893 | Spawning: White Pikmin |
| 14 | Debug | LethalMin | 14838-14894 | Spawning Pikmin (<int>) iteration(<int>) (x1) at: [(<float>, <float>, <float>), (<float>, <float>, <float>, <float>)] With type: White Pikmin odds:(<float>) rng: (<float> / <float>) |
| 14 | Debug | LethalMin | 15135-15370 | White Pikmin: No sound pack found for generation Pikmin4, using default sound pack. |
| 14 | Warning | Unity Log | 15156-15374 | WhitePikmin4 Pik Animation State '' not found |
| 12 | Debug | GeneralImprovements | 685-2004 | Patching Terminal.ParsePlayerSentence to set dropship item limit to 24. |
| 12 | Debug | Buttery Fixes | 750-3641 | Transpiler (RoundManager.GenerateNewLevelClientRpc): Cache mold manager |
| 12 | Debug | Coroner | 936-2377 | Injecting patch #<int> into Landmine.SpawnExplosion... |
| 12 | Debug | Coroner | 937-2378 | Success. |
| 12 | Info | LethalPerformance.Patcher | 4637-15078 | Saved <int> config(s) |
| 12 | Info | Unity Log | 8693-8759 | DropAllHeldItems called on player 'Player #<int>'; itemsFall: False; disconnecting: False; ItemSlots length: <int>; isHoldingObject: False |
| 12 | Info | Unity Log | 8694-8760 | DropAllHeldItems; player pos: (<float>, <float>, <float>) |
| 11 | Debug | ReXuvination | 8790-14149 | Optimised Collider layers in InteractTrigger for Object: Cube (UnityEngine.GameObject) |
| 11 | Info | Unity Log | 17720-17845 | Interact trigger destroying! name: Cube |
| 10 | Debug | LethalMin | 2679-3157 | PikminPrimaryColor set to RGBA(<float>, <float>, <float>, <float>) |
| 10 | Debug | LethalMin | 2680-3158 | PikminSecondaryColor set to RGBA(<float>, <float>, <float>, <float>) |
| 10 | Debug | LethalMin | 2681-3159 | Skipping unsupported field type: PikminIcon (UnityEngine.Sprite) |
| 10 | Debug | LethalMin | 2682-3160 | Skipping unsupported field type: AnimatedPikminGhostTexture (UnityEngine.Texture2D[]) |
| 10 | Debug | LethalMin | 2683-3161 | AnimatedPikminGhostFrameHold set to <int> |
| 10 | Debug | LethalMin | 2684-3162 | OverrideGhostTextureTileing set to (<float>, <float>) |
| 10 | Debug | LethalMin | 2685-3163 | OverrideGhostTextureOffset set to (<float>, <float>) |
| 10 | Debug | LethalMin | 2687-3165 | DisableRegistration set to False |
| 10 | Debug | LethalMin | 2690-3168 | OverrideSproutGlowColor set to RGBA(<float>, <float>, <float>, <float>) |
| 10 | Debug | LethalMin | 2691-3169 | growSpeeds set to System.Collections.Generic.List`<int>[System.Single] |
| 10 | Debug | LethalMin | 2692-3170 | growAttacks set to System.Collections.Generic.List`<int>[System.Single] |
| 10 | Debug | LethalMin | 2693-3171 | growCarryStrengths set to System.Collections.Generic.List`<int>[System.Int32] |
| 10 | Debug | LethalMin | 2694-3172 | GrowSpeedMultiplier set to <int> |
| 10 | Debug | LethalMin | 2695-3173 | DefaultSpeed set to <int> |
| 10 | Debug | LethalMin | 2696-3174 | RunningSpeedMultiplier set to <float> |
| 10 | Debug | LethalMin | 2697-3175 | CarryStrength set to <int> |
| 10 | Debug | LethalMin | 2698-3176 | ThrowForce set to (<float>, <float>, <float>) |
| 10 | Debug | LethalMin | 2699-3177 | HazardsResistantTo set to System.Collections.Generic.List`<int>[PikminHazard] |
| 10 | Debug | LethalMin | 2700-3178 | ItemDetectionRange set to <int> |
| 10 | Debug | LethalMin | 2703-3181 | CanCarryObjects set to True |
| 10 | Debug | LethalMin | 2705-3183 | AttackRate set to <float> |
| 10 | Debug | LethalMin | 2706-3184 | AttackDistance set to <float> |
| 10 | Debug | LethalMin | 2707-3185 | JumpLatchOnRange set to <int> |
| 10 | Debug | LethalMin | 2708-3186 | DamageDeltUponDeath set to <int> |
| 10 | Debug | LethalMin | 2709-3187 | DeathDamageRange set to <int> |
| 10 | Debug | LethalMin | 2710-3188 | DamageDeltUpLanding set to <int> |
| 10 | Debug | LethalMin | 2711-3189 | ShakeEndurance set to <float> |
| 10 | Debug | LethalMin | 2716-3194 | SpawnAfterDay set to <int> |
