from pathlib import Path
import subprocess

BASE = "e042c576ae8985d42172463c86d033fd20d0dcc6"
BRANCH = "work/mouthdog-successor-implementation"
PLUGIN = Path("Patches/S139CompatibilityFixes/Plugin.cs")
WORKFLOW = Path(".github/workflows/temp-mouthdog-successor-cleanup.yml")
SELF = Path("RepositoryTools/temp_mouthdog_successor_cleanup.py")


def run(*args, capture=False):
    if capture:
        return subprocess.check_output(args, text=True)
    subprocess.check_call(args)


text = run("git", "show", f"{BASE}:{PLUGIN.as_posix()}", capture=True)

anchor_call = """            PatchLethalMinEnemyGrabPrevention();
            PatchMouthDogPikminProtection();
            PatchBaboonHawkPikminProtection();"""
replacement_call = """            PatchLethalMinEnemyGrabPrevention();
            PatchMouthDogPikminProtection();
            PatchMouthDogVanillaCollisionProtection();
            PatchBaboonHawkPikminProtection();"""
assert text.count(anchor_call) == 1, text.count(anchor_call)
text = text.replace(anchor_call, replacement_call, 1)

anchor_method = """        private void PatchLethalMinLatchedDeadTargetCompletion()
        {"""
new_method = """        private void PatchMouthDogVanillaCollisionProtection()
        {
            Type pikminAiType = AccessTools.TypeByName(\"LethalMin.PikminAI\");
            if (pikminAiType == null ||
                !string.Equals(pikminAiType.FullName, \"LethalMin.PikminAI\", StringComparison.Ordinal) ||
                !typeof(EnemyAI).IsAssignableFrom(pikminAiType))
            {
                Logger.LogError(
                    \"[MouthDogVanillaCollisionGuard] Exact runtime LethalMin.PikminAI : EnemyAI contract did not validate. \" +
                    \"Vanilla MouthDog collision protection is NOT active; refusing a guessed fallback.\");
                return;
            }

            Type mouthDogType = typeof(MouthDogAI);
            MethodInfo onCollideWithEnemy = mouthDogType.GetMethod(
                \"OnCollideWithEnemy\",
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                new Type[] { typeof(Collider), typeof(EnemyAI) },
                null);

            ParameterInfo[] parameters = onCollideWithEnemy?.GetParameters();
            bool valid =
                onCollideWithEnemy != null &&
                onCollideWithEnemy.DeclaringType == mouthDogType &&
                !onCollideWithEnemy.IsStatic &&
                onCollideWithEnemy.ReturnType == typeof(void) &&
                parameters != null &&
                parameters.Length == 2 &&
                parameters[0].ParameterType == typeof(Collider) &&
                parameters[1].ParameterType == typeof(EnemyAI) &&
                onCollideWithEnemy.GetMethodBody() != null;

            if (!valid)
            {
                Logger.LogError(
                    \"[MouthDogVanillaCollisionGuard] Exact declared instance \" +
                    \"MouthDogAI.OnCollideWithEnemy(Collider,EnemyAI) contract did not validate. \" +
                    \"Vanilla MouthDog collision protection is NOT active; refusing a guessed fallback.\");
                return;
            }

            MouthDogVanillaCollisionProtection.PikminAiType = pikminAiType;

            try
            {
                Harmony.Patch(
                    onCollideWithEnemy,
                    prefix: new HarmonyMethod(
                        typeof(MouthDogVanillaCollisionProtection),
                        nameof(MouthDogVanillaCollisionProtection.Prefix))
                    {
                        priority = Priority.First
                    });

                Logger.LogInfo(
                    \"[MouthDogVanillaCollisionGuard] Patched exact declared \" +
                    \"MouthDogAI.OnCollideWithEnemy(Collider,EnemyAI) with a Priority.First prevention-only prefix. \" +
                    \"Only validated runtime LethalMin.PikminAI collisions are skipped; player and non-Pikmin EnemyAI paths pass through unchanged.\");

                Patches patchInfo = Harmony.GetPatchInfo(onCollideWithEnemy);
                string owners = patchInfo == null
                    ? \"<none>\"
                    : string.Join(\",\", patchInfo.Owners.OrderBy(owner => owner, StringComparer.Ordinal).Take(16));
                Logger.LogInfo(
                    $\"[MouthDogVanillaCollisionGuard] Exact-target Harmony co-patch owners=[{owners}].\");
            }
            catch (Exception ex)
            {
                MouthDogVanillaCollisionProtection.PikminAiType = null;
                Logger.LogError(
                    $\"[MouthDogVanillaCollisionGuard] Failed to patch exact MouthDogAI.OnCollideWithEnemy(Collider,EnemyAI): \" +
                    $\"{ex.GetType().Name}: {ex.Message}\");
            }
        }

"""
assert text.count(anchor_method) == 1, text.count(anchor_method)
text = text.replace(anchor_method, new_method + anchor_method, 1)

anchor_class = """    internal static class BaboonHawkPikminProtection
    {"""
new_class = """    internal static class MouthDogVanillaCollisionProtection
    {
        internal static Type PikminAiType;
        private static readonly HashSet<int> LoggedPikminIds = new HashSet<int>();

        public static bool Prefix(EnemyAI collidedEnemy)
        {
            Type pikminAiType = PikminAiType;
            if (collidedEnemy == null ||
                pikminAiType == null ||
                !pikminAiType.IsInstanceOfType(collidedEnemy))
                return true;

            int id = collidedEnemy.GetInstanceID();
            if (id == 0 || LoggedPikminIds.Add(id))
            {
                Plugin.Log.LogWarning(
                    $\"[MouthDogVanillaCollisionGuard] Blocked MouthDogAI.OnCollideWithEnemy for validated \" +
                    $\"{collidedEnemy.GetType().FullName} before generic enemy lunge/cooldown/HitEnemy(2) mutation. \" +
                    \"MouthDog -> player, non-Pikmin EnemyAI collisions, DetectNoise, and native Pikmin -> MouthDog lifecycle remain unchanged.\");
            }

            return false;
        }
    }

"""
assert text.count(anchor_class) == 1, text.count(anchor_class)
text = text.replace(anchor_class, new_class + anchor_class, 1)

PLUGIN.write_text(text, encoding="utf-8", newline="\n")
run("git", "diff", "--check", "--", PLUGIN.as_posix())
numstat = run("git", "diff", "--numstat", BASE, "--", PLUGIN.as_posix(), capture=True).strip().split()
assert len(numstat) >= 2, numstat
additions, deletions = int(numstat[0]), int(numstat[1])
assert additions > 0, additions
assert deletions == 0, deletions

diff = run("git", "diff", BASE, "--", PLUGIN.as_posix(), capture=True)
for required in (
    "PatchMouthDogVanillaCollisionProtection();",
    "BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly",
    "!typeof(EnemyAI).IsAssignableFrom(pikminAiType)",
    "MouthDogAI.OnCollideWithEnemy(Collider,EnemyAI)",
    "priority = Priority.First",
    "!pikminAiType.IsInstanceOfType(collidedEnemy)",
):
    assert required in diff, required
for forbidden in (
    "DetectNoise(",
    "OnCollideWithPlayer(",
    "EnemyAI.OnCollideWithEnemy",
    "enabled = false",
):
    assert forbidden not in diff, forbidden

WORKFLOW.unlink(missing_ok=True)
SELF.unlink(missing_ok=True)
run("git", "config", "user.name", "github-actions[bot]")
run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
run("git", "add", PLUGIN.as_posix(), WORKFLOW.as_posix(), SELF.as_posix())
run("git", "commit", "-m", "Normalize MouthDog successor to exact base delta")
run("git", "push", "origin", f"HEAD:{BRANCH}")
