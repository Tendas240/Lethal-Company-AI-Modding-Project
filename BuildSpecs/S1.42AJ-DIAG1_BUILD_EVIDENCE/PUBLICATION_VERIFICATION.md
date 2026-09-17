# S1.42AJ-DIAG1 reviewed-artifact publication verification

- Source PR: #111, reviewed head `d3155d86c89595cc9ab4b4cda5d8535ec138eae2`.
- Static/build gate: run `35261773897`, artifact `S1.42AJ-DIAG1-review`, artifact ID `10513954928`.
- Artifact ZIP SHA-256: `c9963e7155515426cdeb02b110373ee4252e4f807a7c20430b2c43747e75d7ce`.
- Published profile SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`.
- Published DIAG1 DLL SHA-256: `9a477c18e5b8cf38922fa755b6bab101babc2f987e858567172b9be9c2c05fad`.
- Accepted normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.
- Canonical rebuild run `35264134978` succeeded but produced profile `8c870328971521c4cfb33a4ea75b7453e6bce379219c48086453ad8db962a609` because its freshly compiled diagnostic DLL was `7deab805984bd89a6aef79507dcbdb566f0a2993a5be21605d7def6513422235` instead of the exact reviewed DLL bytes.
- Member-by-member comparison proved all 336 member names/order identical and 335/336 member payloads byte-identical; the diagnostic DLL was the sole byte difference.
- Publication therefore uses the exact already-reviewed CI artifact rather than accepting a non-byte-identical recompilation.
- The reviewed artifact was revalidated during publication against exact balanced S1.42AJ, exact archive delta, all 336 FILE_INDEX records, diagnostic DLL identity and accepted normalizer identity.
- Atomic exact-artifact publication commit: `71ac6fad7eef3eb5e7d84b81e88a553d1032fbdf`; its tree contains the exact reviewed profile/evidence bytes and the restored disabled build controller.
- `BuildSpecs/current.json` is returned to the pre-publication disabled S1.42AJ idle state. `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are intentionally unchanged; runtime/lifecycle preparation is a separate atomic step.

Status remains `STATIC_PASS_NOT_RUNTIME_READY`: runtime caller identification, Harmony execution ordering and LC Office generation/gameplay coverage are not yet proven.
