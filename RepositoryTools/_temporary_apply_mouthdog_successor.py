from pathlib import Path
import re

path = Path("Patches/S139CompatibilityFixes/Plugin.cs")
text = path.read_text(encoding="utf-8")

new_method = '''        private void PatchMouthDogPikminProtection()
        {
            Type mouthDogPikminEnemyType = AccessTools.TypeByName("LethalMin.MouthDogPikminEnemy");
            Type pikminAiType = AccessTools.TypeByName("LethalMin.PikminAI");

            if (mouthDogPikminEnemyType == null || pikminAiType == null)
            {
                Logger.LogError(
                    "[MouthDogPikminGuard] Required exact LethalMin.MouthDogPikminEnemy/LethalMin.PikminAI types were not found. " +
                    "Dual Mouth Dog -> Pikmin prevention is NOT active.");
                return;
            }

            if (!typeof(EnemyAI).IsAssignableFrom(pikminAiType))
            {
                Logger.LogError(
                    "[MouthDogVanillaCollisionGuard] Resolved LethalMin.PikminAI does not derive from EnemyAI. " +
                    "Refusing to install the reviewed collision prefix or any guessed fallback.");
                return;
            }

            MethodInfo doCheckInterval = mouthDogPikminEnemyType.GetMethod(
                "DoCheckInterval",
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                Type.EmptyTypes,
                null);

            bool adapterValid =
                doCheckInterval != null &&
                doCheckInterval.DeclaringType == mouthDogPikminEnemyType &&
                !doCheckInterval.IsStatic &&
                doCheckInterval.ReturnType == typeof(void) &&
                doCheckInterval.GetParameters().Length == 0 &&
                doCheckInterval.GetMethodBody() != null;

            if (!adapterValid)
            {
                Logger.LogError(
                    "[MouthDogPikminGuard] Exact declared instance " +
                    "LethalMin.MouthDogPikminEnemy.DoCheckInterval() contract did not validate. " +
                    "Refusing to install either MouthDog successor hook or a guessed fallback.");
                return;
            }

            MethodInfo onCollideWithEnemy = typeof(MouthDogAI).GetMethod(
                "OnCollideWithEnemy",
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                new Type[] { typeof(Collider), typeof(EnemyAI) },
                null);

            ParameterInfo[] collisionParameters = onCollideWithEnemy?.GetParameters();
            bool collisionValid =
                onCollideWithEnemy != null &&
                onCollideWithEnemy.DeclaringType == typeof(MouthDogAI) &&
                !onCollideWithEnemy.IsStatic &&
                onCollideWithEnemy.ReturnType == typeof(void) &&
                collisionParameters != null &&
                collisionParameters.Length == 2 &&
                collisionParameters[0].ParameterType == typeof(Collider) &&
                collisionParameters[1].ParameterType == typeof(EnemyAI) &&
                onCollideWithEnemy.GetMethodBody() != null;

            if (!collisionValid)
            {
                Logger.LogError(
                    "[MouthDogVanillaCollisionGuard] Exact declared instance " +
                    "MouthDogAI.OnCollideWithEnemy(Collider,EnemyAI) contract did not validate. " +
                    "Refusing to install either MouthDog successor hook or a guessed fallback.");
                return;
            }

            MethodInfo adapterPrefixMethod = AccessTools.Method(
                typeof(MouthDogPikminProtection),
                nameof(MouthDogPikminProtection.Prefix));
            MethodInfo collisionPrefixMethod = AccessTools.Method(
                typeof(MouthDogPikminProtection),
                nameof(MouthDogPikminProtection.BlockVanillaEnemyCollisionPrefix));

            if (adapterPrefixMethod == null || collisionPrefixMethod == null)
            {
                Logger.LogError(
                    "[MouthDogPikminGuard] Local successor prefix methods could not be resolved. " +
                    "Dual Mouth Dog -> Pikmin prevention is NOT active.");
                return;
            }

            MouthDogPikminProtection.PikminAiType = pikminAiType;

            try
            {
                Harmony.Patch(
                    doCheckInterval,
                    prefix: new HarmonyMethod(adapterPrefixMethod)
                    {
                        priority = Priority.First
                    });

                Harmony.Patch(
                    onCollideWithEnemy,
                    prefix: new HarmonyMethod(collisionPrefixMethod)
                    {
                        priority = Priority.First
                    });
            }
            catch (Exception ex)
            {
                MouthDogPikminProtection.PikminAiType = null;

                try
                {
                    Harmony.Unpatch(doCheckInterval, adapterPrefixMethod);
                }
                catch (Exception rollbackEx)
                {
                    Logger.LogError(
                        $"[MouthDogPikminGuard] Adapter rollback after failed dual installation also failed: " +
                        $"{rollbackEx.GetType().Name}: {rollbackEx.Message}");
                }

                try
                {
                    Harmony.Unpatch(onCollideWithEnemy, collisionPrefixMethod);
                }
                catch (Exception rollbackEx)
                {
                    Logger.LogError(
                        $"[MouthDogVanillaCollisionGuard] Collision rollback after failed dual installation also failed: " +
                        $"{rollbackEx.GetType().Name}: {rollbackEx.Message}");
                }

                Logger.LogError(
                    $"[MouthDogPikminGuard] Failed to install the validated dual MouthDog successor contract. " +
                    $"Any local partial hook was rolled back; no guessed fallback will be installed. " +
                    $"{ex.GetType().Name}: {ex.Message}");
                return;
            }

            Logger.LogInfo(
                "[MouthDogPikminGuard] Patched exact declared " +
                "LethalMin.MouthDogPikminEnemy.DoCheckInterval() with a Priority.First prevention-only prefix. " +
                "The adapter remains enabled; native Pikmin -> Mouth Dog combat/lifecycle remains owned by LethalMin.");

            Logger.LogInfo(
                "[MouthDogVanillaCollisionGuard] Patched exact declared " +
                "MouthDogAI.OnCollideWithEnemy(Collider,EnemyAI) with a Priority.First prevention-only prefix. " +
                "Only validated runtime LethalMin.PikminAI collisions are skipped; null and non-Pikmin EnemyAI pass through unchanged.");

            MouthDogPikminProtection.LogCollisionPatchOwners(onCollideWithEnemy);
        }
'''

method_pattern = re.compile(
    r'        private void PatchMouthDogPikminProtection\(\)\n'
    r'        \{.*?\n'
    r'        \}\n\n'
    r'        private void PatchLethalMinLatchedDeadTargetCompletion\(\)',
    re.S,
)
text, method_count = method_pattern.subn(
    lambda _: new_method + '\n        private void PatchLethalMinLatchedDeadTargetCompletion()',
    text,
    count=1,
)
if method_count != 1:
    raise SystemExit(f"Expected exactly one PatchMouthDogPikminProtection region, replaced {method_count}")

new_class = '''    internal static class MouthDogPikminProtection
    {
        internal static Type PikminAiType;

        private const int MaxCollisionBlockLogs = 8;
        private static readonly HashSet<int> LoggedAdapterIds = new HashSet<int>();
        private static int CollisionBlockLogCount;

        public static bool Prefix(object __instance)
        {
            int id = 0;
            if (__instance is UnityEngine.Object unityObject && unityObject != null)
                id = unityObject.GetInstanceID();

            if (id == 0 || LoggedAdapterIds.Add(id))
            {
                Plugin.Log.LogWarning(
                    "[MouthDogPikminGuard] Blocked LethalMin MouthDogPikminEnemy.DoCheckInterval before " +
                    "Pikmin target collection, bite RPC dispatch, GrabbedPikmin bookkeeping, or GrabPikmin state mutation. " +
                    "MouthDogPikminEnemy remains enabled for native reverse-direction lifecycle handling.");
            }

            return false;
        }

        public static bool BlockVanillaEnemyCollisionPrefix(EnemyAI collidedEnemy)
        {
            Type pikminAiType = PikminAiType;
            if (collidedEnemy == null ||
                pikminAiType == null ||
                !pikminAiType.IsInstanceOfType(collidedEnemy))
                return true;

            if (CollisionBlockLogCount < MaxCollisionBlockLogs)
            {
                CollisionBlockLogCount++;
                Plugin.Log.LogWarning(
                    $"[MouthDogVanillaCollisionGuard] Blocked exact MouthDogAI.OnCollideWithEnemy collision for " +
                    $"validated {pikminAiType.FullName} instanceId={collidedEnemy.GetInstanceID()} " +
                    $"({CollisionBlockLogCount}/{MaxCollisionBlockLogs} bounded markers). " +
                    "The Dog override is skipped before generic-enemy lunge/cooldown/HitEnemy(2) mutation; " +
                    "non-Pikmin EnemyAI and MouthDog -> player remain unchanged.");
            }

            return false;
        }

        internal static void LogCollisionPatchOwners(MethodInfo target)
        {
            if (target == null)
                return;

            try
            {
                Patches patchInfo = Harmony.GetPatchInfo(target);
                if (patchInfo == null)
                {
                    Plugin.Log.LogWarning(
                        "[MouthDogVanillaCollisionGuard] Exact target PatchInfo was unexpectedly empty after installation.");
                    return;
                }

                Plugin.Log.LogInfo(
                    "[MouthDogVanillaCollisionGuard] Exact target co-patch ownership: " +
                    $"prefixes=[{DescribeOwners(patchInfo.Prefixes)}]; " +
                    $"postfixes=[{DescribeOwners(patchInfo.Postfixes)}]; " +
                    $"transpilers=[{DescribeOwners(patchInfo.Transpilers)}]; " +
                    $"finalizers=[{DescribeOwners(patchInfo.Finalizers)}].");
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning(
                    $"[MouthDogVanillaCollisionGuard] Could not read bounded PatchInfo for the exact collision target: " +
                    $"{ex.GetType().Name}: {ex.Message}");
            }
        }

        private static string DescribeOwners(IEnumerable<Patch> patches)
        {
            if (patches == null)
                return "<none>";

            string[] owners = patches
                .Where(p => p != null)
                .Select(p => string.IsNullOrWhiteSpace(p.owner) ? "<unknown>" : p.owner)
                .Distinct(StringComparer.Ordinal)
                .OrderBy(owner => owner, StringComparer.Ordinal)
                .ToArray();

            return owners.Length == 0 ? "<none>" : string.Join(",", owners);
        }
    }
'''

class_pattern = re.compile(
    r'    internal static class MouthDogPikminProtection\n'
    r'    \{.*?\n'
    r'    \}\n\n'
    r'    internal static class BaboonHawkPikminProtection',
    re.S,
)
text, class_count = class_pattern.subn(
    lambda _: new_class + '\n    internal static class BaboonHawkPikminProtection',
    text,
    count=1,
)
if class_count != 1:
    raise SystemExit(f"Expected exactly one MouthDogPikminProtection class region, replaced {class_count}")

required = [
    'AccessTools.TypeByName("LethalMin.MouthDogPikminEnemy")',
    'AccessTools.TypeByName("LethalMin.PikminAI")',
    'typeof(EnemyAI).IsAssignableFrom(pikminAiType)',
    'typeof(MouthDogAI).GetMethod(',
    'new Type[] { typeof(Collider), typeof(EnemyAI) }',
    'nameof(MouthDogPikminProtection.BlockVanillaEnemyCollisionPrefix)',
    'pikminAiType.IsInstanceOfType(collidedEnemy)',
    'Harmony.GetPatchInfo(target)',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit("Missing required successor markers: " + repr(missing))

forbidden = [
    'MouthDogAI.DetectNoise',
    'nameof(MouthDogAI.DetectNoise)',
]
present = [marker for marker in forbidden if marker in text]
if present:
    raise SystemExit("Forbidden successor markers present: " + repr(present))

path.write_text(text, encoding="utf-8", newline="\n")
