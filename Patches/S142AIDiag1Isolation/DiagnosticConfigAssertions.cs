using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using BepInEx;

namespace S142AIDiag1Isolation
{
    /// <summary>
    /// Read-only runtime proof for the temporary DIAG1 config overlay. This code never
    /// repairs or rewrites configuration; any missing, duplicate or contradictory key
    /// marks the diagnostic invalid so the runtime log cannot silently claim isolation.
    /// </summary>
    internal static class DiagnosticConfigAssertions
    {
        private const string BcmerRoot = "BrutalCompanyMinusExtraReborn";

        internal static bool AssertAll()
        {
            bool valid = true;
            valid &= AssertBcmerEvents();
            valid &= AssertBcmerCore();
            valid &= AssertBcmerDifficulty();
            valid &= AssertExact("ArcadiaMoonPlugin.cfg", "Spawning", "ForceSpawnFlowerman", "false");
            valid &= AssertExact("ArcadiaMoonPlugin.cfg", "Spawning", "ForceSpawnBaboon", "false");
            valid &= AssertExact("ArcadiaMoonPlugin.cfg", "Spawning", "ForceSpawnRadMech", "false");
            valid &= AssertExact("butterystancakes.lethalcompany.butterybalance.cfg", "Infestations", "Rework Mechanics", "false");
            valid &= AssertExact("me.biodiversity.junk_radar.cfg", "_General", "Enabled", "false");
            valid &= AssertExact("me.biodiversity.ogopogo.cfg", "Vermin", "EnableVermin", "false");
            valid &= AssertExact("me.biodiversity.ogopogo.cfg", "Vermin", "OgopogoEnabled", "false");
            valid &= AssertExact("sparble.slendermanmod.cfg", "PageItem.Values", "Page Spawning", "");
            valid &= AssertExact("sparble.slendermanmod.cfg", "Slenderman", "Natural Spawn Chances", "0");
            valid &= AssertExact("NoteBoxz.LethalMin.cfg", "Spawning", "Indoor Pikmin Spawn Chance", "0");
            valid &= AssertExact("NoteBoxz.LethalMin.cfg", "Spawning", "Outdoor Pikmin Spawn Chance", "0");
            valid &= AssertExact("NoteBoxz.LethalMin.cfg", "Spawning", "Onion Spawn Chance", "0");
            valid &= AssertExact("NoteBoxz.LethalMin.cfg", "Glow Pikmin", "Spawn Chance", "0");
            valid &= AssertExact("Mirage.General.cfg", "Spawn control", "Enable spawn control (masked enemies)", "false");

            if (Plugin.DiagnosticEnabled == null || !Plugin.DiagnosticEnabled.Value)
            {
                Invalid("Plugin self config is not enabled while DIAG1 startup assertions are running.");
                valid = false;
            }
            else
            {
                Plugin.Log.LogInfo("[DIAG1_CONFIG_VERIFIED] tendas.s142ai.diag1.isolation.cfg: Diagnostics / S1.42AI-DIAG1 Enabled = true");
            }

            if (valid)
                Plugin.Log.LogInfo("[DIAG1_CONFIG_OVERLAY_VERIFIED] All approved DIAG1 config gates and preserved BCMER values validated read-only.");
            return valid;
        }

        private static bool AssertBcmerEvents()
        {
            IniDocument vanilla;
            IniDocument modded;
            if (!TryLoad(Path.Combine(BcmerRoot, "VanillaEvents.cfg"), out vanilla) ||
                !TryLoad(Path.Combine(BcmerRoot, "ModdedEvents.cfg"), out modded))
                return false;

            bool valid = true;
            int vanillaCount = 0;
            foreach (KeyValuePair<string, Dictionary<string, string>> section in vanilla.Sections)
            {
                string enabled;
                if (!section.Value.TryGetValue("Event Enabled?", out enabled))
                    continue;
                vanillaCount++;
                if (!string.Equals(enabled, "false", StringComparison.OrdinalIgnoreCase))
                {
                    Invalid($"VanillaEvents.cfg [{section.Key}] Event Enabled? must be false, got '{enabled}'.");
                    valid = false;
                }
            }

            int moddedCount = 0;
            int enabledCount = 0;
            string enabledSection = null;
            foreach (KeyValuePair<string, Dictionary<string, string>> section in modded.Sections)
            {
                string enabled;
                if (!section.Value.TryGetValue("Event Enabled?", out enabled))
                    continue;
                moddedCount++;
                bool isEnabled;
                if (!bool.TryParse(enabled, out isEnabled))
                {
                    Invalid($"ModdedEvents.cfg [{section.Key}] Event Enabled? is not Boolean: '{enabled}'.");
                    valid = false;
                    continue;
                }
                if (isEnabled)
                {
                    enabledCount++;
                    enabledSection = section.Key;
                }
                if (!string.Equals(section.Key, "ShyGuy", StringComparison.Ordinal) && isEnabled)
                {
                    Invalid($"Non-allowlisted BCMER event [{section.Key}] remains enabled.");
                    valid = false;
                }
            }

            if (vanillaCount == 0 || moddedCount == 0)
            {
                Invalid($"BCMER event inventory unexpectedly empty: vanilla={vanillaCount}, modded={moddedCount}.");
                valid = false;
            }
            if (enabledCount != 1 || !string.Equals(enabledSection, "ShyGuy", StringComparison.Ordinal))
            {
                Invalid($"BCMER allowlist must contain exactly one enabled event [ShyGuy]; enabledCount={enabledCount}, enabledSection='{enabledSection ?? "<none>"}'.");
                valid = false;
            }

            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "Event Type", "VeryBad");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "Events To Spawn With", "");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "Enemy 0 Name", "ShyGuyDef");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "ShyGuyDef InsideEnemyRarity", "20, 0.8, 20, 100");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "ShyGuyDef OutsideEnemyRarity", "0, 0, 0, 0");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "ShyGuyDef MinInsideEnemy", "2, 0.04, 2, 6");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "ShyGuyDef MaxInsideEnemy", "2, 0.04, 2, 6");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "ShyGuyDef MinOutsideEnemy", "0, 0, 0, 0");
            valid &= Expect(modded, "ModdedEvents.cfg", "ShyGuy", "ShyGuyDef MaxOutsideEnemy", "0, 0, 0, 0");

            string customPath = ConfigPath(Path.Combine(BcmerRoot, "CustomEvents.cfg"));
            try
            {
                if (!File.Exists(customPath) || File.ReadAllBytes(customPath).Length != 0)
                {
                    Invalid("BCMER CustomEvents.cfg must remain the exact empty file for DIAG1.");
                    valid = false;
                }
            }
            catch (Exception ex)
            {
                Invalid($"Could not read BCMER CustomEvents.cfg: {ex.GetType().Name}: {ex.Message}");
                valid = false;
            }

            if (valid)
                Plugin.Log.LogInfo($"[DIAG1_CONFIG_VERIFIED] BCMER events: vanilla={vanillaCount} all disabled; modded={moddedCount}; exactly [ShyGuy] enabled with preserved interior/exterior contract; CustomEvents.cfg empty.");
            return valid;
        }

        private static bool AssertBcmerCore()
        {
            IniDocument core;
            if (!TryLoad(Path.Combine(BcmerRoot, "CoreProperties.cfg"), out core))
                return false;

            bool valid = true;
            valid &= Expect(core, "CoreProperties.cfg", "Custom Events", "Enable Custom Events?", "false");
            valid &= Expect(core, "CoreProperties.cfg", "Events Features", "Disable all events?", "false");
            valid &= Expect(core, "CoreProperties.cfg", "Events Features", "Chance of Events Occurring", "100, 0.0, 100, 100");
            valid &= Expect(core, "CoreProperties.cfg", "Events Features", "Enable Special Events?", "false");
            valid &= Expect(core, "CoreProperties.cfg", "Events Features", "Enable Beta Events?", "false");
            valid &= Expect(core, "CoreProperties.cfg", "Randomizer", "Enable Randomizer?", "false");
            if (valid)
                Plugin.Log.LogInfo("[DIAG1_CONFIG_VERIFIED] BCMER CoreProperties: custom/special/beta/randomizer disabled; normal event execution remains enabled at 100%.");
            return valid;
        }

        private static bool AssertBcmerDifficulty()
        {
            IniDocument difficulty;
            if (!TryLoad(Path.Combine(BcmerRoot, "Difficulty_Settings.cfg"), out difficulty))
                return false;

            bool valid = true;
            valid &= Expect(difficulty, "Difficulty_Settings.cfg", "_Event Settings", "Event scale amount", "1, 0, 1, 1");
            valid &= Expect(difficulty, "Difficulty_Settings.cfg", "_Event Settings", "Weights for bonus events", "1, 0, 0, 0, 0");
            valid &= Expect(difficulty, "Difficulty_Settings.cfg", "_Event Settings", "Use custom weights?", "false");
            foreach (string eventType in new[] { "Insane", "VeryBad", "Bad", "Neutral", "Good", "VeryGood", "Rare", "Remove" })
                valid &= Expect(difficulty, "Difficulty_Settings.cfg", "_EventType Weights", eventType + " event scale", "12.5, 0.0, 12.5, 12.5");
            valid &= ExpectUnique(difficulty, "Difficulty_Settings.cfg", "Scale by Heat?", "false");
            valid &= ExpectUnique(difficulty, "Difficulty_Settings.cfg", "Force event at max heat?", "false");
            valid &= ExpectUnique(difficulty, "Difficulty_Settings.cfg", "Events to force at max heat", "");
            if (valid)
                Plugin.Log.LogInfo("[DIAG1_CONFIG_VERIFIED] BCMER Difficulty: exactly one normal draw, zero bonus draws, accepted EventType weights preserved, heat forcing disabled.");
            return valid;
        }

        private static bool AssertExact(string relativePath, string section, string key, string expected)
        {
            IniDocument doc;
            if (!TryLoad(relativePath, out doc))
                return false;
            bool valid = Expect(doc, relativePath, section, key, expected);
            if (valid)
                Plugin.Log.LogInfo($"[DIAG1_CONFIG_VERIFIED] {relativePath}: [{section}] {key} = {expected}");
            return valid;
        }

        private static bool TryLoad(string relativePath, out IniDocument document)
        {
            document = null;
            string path = ConfigPath(relativePath);
            try
            {
                document = IniDocument.Load(path);
                return true;
            }
            catch (Exception ex)
            {
                Invalid($"Failed to parse config '{relativePath}': {ex.GetType().Name}: {ex.Message}");
                return false;
            }
        }

        private static bool Expect(IniDocument doc, string label, string section, string key, string expected)
        {
            string actual;
            if (!doc.TryGet(section, key, out actual))
            {
                Invalid($"{label}: missing exact [{section}] {key}.");
                return false;
            }
            if (!string.Equals(actual, expected, StringComparison.Ordinal))
            {
                Invalid($"{label}: [{section}] {key} expected '{expected}', got '{actual}'.");
                return false;
            }
            return true;
        }

        private static bool ExpectUnique(IniDocument doc, string label, string key, string expected)
        {
            List<KeyValuePair<string, string>> matches = doc.FindKey(key).ToList();
            if (matches.Count != 1)
            {
                Invalid($"{label}: key '{key}' expected exactly once, found {matches.Count}.");
                return false;
            }
            if (!string.Equals(matches[0].Value, expected, StringComparison.Ordinal))
            {
                Invalid($"{label}: [{matches[0].Key}] {key} expected '{expected}', got '{matches[0].Value}'.");
                return false;
            }
            return true;
        }

        private static string ConfigPath(string relativePath)
        {
            return Path.Combine(Paths.ConfigPath, relativePath.Replace('/', Path.DirectorySeparatorChar));
        }

        private static void Invalid(string message)
        {
            DiagnosticIsolation.MarkInvalid("[DIAG1_CONFIG_INVALID] " + message);
        }

        private sealed class IniDocument
        {
            internal readonly Dictionary<string, Dictionary<string, string>> Sections =
                new Dictionary<string, Dictionary<string, string>>(StringComparer.Ordinal);

            internal static IniDocument Load(string path)
            {
                if (!File.Exists(path))
                    throw new FileNotFoundException("Config file was not found.", path);

                IniDocument doc = new IniDocument();
                Dictionary<string, string> current = null;
                string currentName = null;
                int lineNumber = 0;
                foreach (string raw in File.ReadAllLines(path))
                {
                    lineNumber++;
                    string line = raw.Trim();
                    if (line.Length == 0 || line.StartsWith("#", StringComparison.Ordinal) || line.StartsWith(";", StringComparison.Ordinal))
                        continue;
                    if (line.StartsWith("[", StringComparison.Ordinal) && line.EndsWith("]", StringComparison.Ordinal))
                    {
                        currentName = line.Substring(1, line.Length - 2).Trim();
                        if (currentName.Length == 0 || doc.Sections.ContainsKey(currentName))
                            throw new InvalidDataException($"Duplicate/invalid section [{currentName}] at line {lineNumber}.");
                        current = new Dictionary<string, string>(StringComparer.Ordinal);
                        doc.Sections.Add(currentName, current);
                        continue;
                    }
                    int equals = raw.IndexOf('=');
                    if (equals < 0 || current == null)
                        throw new InvalidDataException($"Unparsed config data at line {lineNumber}: {raw}");
                    string key = raw.Substring(0, equals).Trim();
                    string value = raw.Substring(equals + 1).Trim();
                    if (current.ContainsKey(key))
                        throw new InvalidDataException($"Duplicate key [{currentName}] {key} at line {lineNumber}.");
                    current.Add(key, value);
                }
                return doc;
            }

            internal bool TryGet(string section, string key, out string value)
            {
                value = null;
                Dictionary<string, string> data;
                return Sections.TryGetValue(section, out data) && data.TryGetValue(key, out value);
            }

            internal IEnumerable<KeyValuePair<string, string>> FindKey(string key)
            {
                foreach (KeyValuePair<string, Dictionary<string, string>> section in Sections)
                {
                    string value;
                    if (section.Value.TryGetValue(key, out value))
                        yield return new KeyValuePair<string, string>(section.Key, value);
                }
            }
        }
    }
}
