using System;
using System.Collections;
using System.Reflection;
using BepInEx.Bootstrap;
using BepInEx.Configuration;
using HarmonyLib;

namespace S142AIDiag1Isolation
{
    /// <summary>
    /// Runtime/startup assertions whose exact facts are closed by the S1.42AI-DIAG1
    /// source reviews and approved temporary config overlay. All checks are read-only;
    /// a mismatch marks the diagnostic invalid rather than mutating foreign state.
    /// </summary>
    internal static class DiagnosticStartupAssertions
    {
        private const string MoreCompanyTypeName = "MoreCompany.DebugCommandRegistry";
        private const string SnowyLibPluginTypeName = "SnowyLib.Plugin";
        private const string EmergencyDiceGuid = "Theronguard.EmergencyDice";
        private const string S139PluginGuid = "tendas.s139.compatibilityfixes";
        private const string S139ExpectedVersion = "1.3.14";
        private const string S139IsolationTypeName = "S139CompatibilityFixes.DiagnosticEnemyIsolation";

        internal static IEnumerator RunAfterPluginAwake()
        {
            // Wait one frame so foreign BepInEx Awake methods have initialized their
            // exact config/static fields before we read them. This is a one-shot
            // startup assertion, not a per-frame poll.
            yield return null;

            bool valid = true;
            valid &= DiagnosticConfigAssertions.AssertAll();
            valid &= AssertMoreCompanyCommandDisabled();
            valid &= AssertSnowyLibTestingDisabled();
            AnchorInteractiveTerminalNoConsumerEvidence();
            valid &= AssertEmergencyDiceProviderAbsent();
            valid &= AssertLegacyS139IsolationDisabled();

            if (valid)
            {
                Plugin.Log.LogInfo(
                    "[DIAG1_STARTUP_ASSERTIONS_OK] approved config overlay verified; MoreCompany debug command disabled; " +
                    "SnowyLib testing disabled; InteractiveTerminal/SnowyLib no-consumer evidence anchored; " +
                    "EmergencyDice provider absent; legacy S139 isolated-enemy diagnostic disabled.");
                yield break;
            }

            DiagnosticIsolation.MarkInvalid(
                "One or more exact DIAG1 startup/environment/config assertions failed. " +
                "The run is diagnostic-invalid; no fallback, repair or widened patch set is permitted.");
        }

        private static bool AssertMoreCompanyCommandDisabled()
        {
            Type owner = AccessTools.TypeByName(MoreCompanyTypeName);
            FieldInfo field = owner?.GetField(
                "commandEnabled",
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);

            if (owner == null ||
                field == null ||
                field.DeclaringType != owner ||
                !field.IsStatic ||
                field.FieldType != typeof(bool))
            {
                Plugin.Log.LogError(
                    "[DIAG1_MORECOMPANY_ASSERT_INVALID] Exact MoreCompany.DebugCommandRegistry.commandEnabled static bool field was not found.");
                return false;
            }

            bool enabled;
            try
            {
                enabled = (bool)field.GetValue(null);
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_MORECOMPANY_ASSERT_INVALID] Failed to read commandEnabled: {ex.GetType().Name}: {ex.Message}");
                return false;
            }

            if (enabled)
            {
                Plugin.Log.LogError(
                    "[DIAG1_MORECOMPANY_COMMAND_ENABLED] MoreCompany debug command is enabled; DIAG1 cannot assume the reviewed dormant spawn-command route.");
                return false;
            }

            Plugin.Log.LogInfo(
                "[DIAG1_MORECOMPANY_COMMAND_DISABLED] MoreCompany.DebugCommandRegistry.commandEnabled=false; " +
                "exact direct-owner review run=34705834727.");
            return true;
        }

        private static bool AssertSnowyLibTestingDisabled()
        {
            Type owner = AccessTools.TypeByName(SnowyLibPluginTypeName);
            FieldInfo field = owner?.GetField(
                "cfgTesting",
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);

            if (owner == null ||
                field == null ||
                field.DeclaringType != owner ||
                !field.IsStatic ||
                field.FieldType != typeof(ConfigEntry<bool>))
            {
                Plugin.Log.LogError(
                    "[DIAG1_SNOWYLIB_ASSERT_INVALID] Exact SnowyLib.Plugin.cfgTesting ConfigEntry<bool> field was not found.");
                return false;
            }

            ConfigEntry<bool> testing;
            try
            {
                testing = field.GetValue(null) as ConfigEntry<bool>;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_SNOWYLIB_ASSERT_INVALID] Failed to read cfgTesting: {ex.GetType().Name}: {ex.Message}");
                return false;
            }

            if (testing == null)
            {
                Plugin.Log.LogError(
                    "[DIAG1_SNOWYLIB_ASSERT_INVALID] SnowyLib.Plugin.cfgTesting was null after the one-frame plugin-Awake barrier.");
                return false;
            }

            if (testing.Value)
            {
                Plugin.Log.LogError(
                    "[DIAG1_SNOWYLIB_TESTING_ENABLED] SnowyLib [Debugging] Testing=true; its reviewed /spawnenemy route is therefore not dormant.");
                return false;
            }

            Plugin.Log.LogInfo(
                "[DIAG1_SNOWYLIB_TESTING_DISABLED] SnowyLib 1.13.1 [Debugging] Testing=false; " +
                "cross-assembly no-consumer evidence anchored to run=34715820639, externalConsumers=0.");
            return true;
        }

        private static void AnchorInteractiveTerminalNoConsumerEvidence()
        {
            Plugin.Log.LogInfo(
                "[DIAG1_INTERACTIVE_TERMINAL_NO_CONSUMER_EVIDENCE] " +
                "WhiteSpike-Interactive_Terminal_API 1.3.3; exact installed-set cross-assembly review run=34715820639; " +
                "external SpawnMob consumers=0. Any package/version/profile change reopens this assertion.");
        }

        private static bool AssertEmergencyDiceProviderAbsent()
        {
            if (Chainloader.PluginInfos.ContainsKey(EmergencyDiceGuid))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_EMERGENCY_DICE_PRESENT] Provider GUID '{EmergencyDiceGuid}' is loaded. " +
                    "The reviewed Bozoros Puffer/Butler dice routes are no longer dormant; DIAG1 is invalid rather than widening its patch set.");
                return false;
            }

            Plugin.Log.LogInfo(
                $"[DIAG1_EMERGENCY_DICE_ABSENT] Provider GUID '{EmergencyDiceGuid}' is absent; " +
                "exact Bozoros Tier-B review run=34709775849.");
            return true;
        }

        private static bool AssertLegacyS139IsolationDisabled()
        {
            if (!Chainloader.PluginInfos.TryGetValue(S139PluginGuid, out var pluginInfo))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_S139_ASSERT_INVALID] Required existing plugin '{S139PluginGuid}' is not loaded.");
                return false;
            }

            string version = pluginInfo?.Metadata?.Version?.ToString() ?? "<null>";
            if (!string.Equals(version, S139ExpectedVersion, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_S139_ASSERT_INVALID] Loaded S139CompatibilityFixes version '{version}' != expected '{S139ExpectedVersion}'.");
                return false;
            }

            Type owner = AccessTools.TypeByName(S139IsolationTypeName);
            FieldInfo field = owner?.GetField(
                "Enabled",
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);

            if (owner == null ||
                field == null ||
                field.DeclaringType != owner ||
                !field.IsStatic ||
                field.FieldType != typeof(bool))
            {
                Plugin.Log.LogError(
                    "[DIAG1_S139_ASSERT_INVALID] Exact S139CompatibilityFixes.DiagnosticEnemyIsolation.Enabled static bool field was not found.");
                return false;
            }

            bool enabled;
            try
            {
                enabled = (bool)field.GetValue(null);
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_S139_ASSERT_INVALID] Failed to read legacy DiagnosticEnemyIsolation.Enabled: {ex.GetType().Name}: {ex.Message}");
                return false;
            }

            if (enabled)
            {
                Plugin.Log.LogError(
                    "[DIAG1_LEGACY_ISOLATION_ENABLED] S139 Diagnostics / Isolated Enemy Regression=true. " +
                    "The legacy Thumper/Puffer/Baboon/Pikmin allowlist must not overlap DIAG1.");
                return false;
            }

            Plugin.Log.LogInfo(
                $"[DIAG1_LEGACY_ISOLATION_DISABLED] '{S139PluginGuid}' version={version}; " +
                "Diagnostics / Isolated Enemy Regression=false; legacy Thumper/Puffer/Baboon/Pikmin allowlist inactive.");
            return true;
        }
    }
}
