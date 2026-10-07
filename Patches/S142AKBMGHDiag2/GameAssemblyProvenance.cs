using System;
using System.IO;
using System.Security.Cryptography;

namespace S142AKBMGHDiag2
{
    // Installed-source provenance only. This helper never inspects a loaded Assembly object.
    internal static class GameAssemblyProvenance
    {
        internal const string FileName = "Assembly-CSharp.dll";

        internal static string Validate(string managedPath, string expectedSha256, Func<string, Stream> openRead = null)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(managedPath))
                    throw new InvalidOperationException("BepInEx managed path is blank.");
                if (!IsLowerHexSha256(expectedSha256))
                    throw new InvalidOperationException("Expected installed game SHA-256 is malformed.");

                string canonicalManagedPath = Path.GetFullPath(managedPath);
                if (!Directory.Exists(canonicalManagedPath))
                    throw new InvalidOperationException("BepInEx managed directory does not exist.");

                string assemblyPath = Path.Combine(canonicalManagedPath, FileName);
                if (!File.Exists(assemblyPath))
                    throw new InvalidOperationException("Exact installed Assembly-CSharp.dll is missing from BepInEx managed path.");

                using (Stream stream = openRead == null
                    ? new FileStream(assemblyPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete)
                    : openRead(assemblyPath))
                {
                    if (stream == null || !stream.CanRead)
                        throw new InvalidOperationException("Exact installed Assembly-CSharp.dll is not readable.");
                    using (SHA256 sha = SHA256.Create())
                    {
                        string actual = BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", "").ToLowerInvariant();
                        if (actual != expectedSha256)
                            throw new InvalidOperationException("Installed Assembly-CSharp.dll SHA-256 mismatch: got " + actual);
                        return actual;
                    }
                }
            }
            catch (InvalidOperationException)
            {
                throw;
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException("Installed Assembly-CSharp.dll provenance validation failed.", ex);
            }
        }

        private static bool IsLowerHexSha256(string value)
        {
            if (value == null || value.Length != 64)
                return false;
            for (int i = 0; i < value.Length; i++)
            {
                char c = value[i];
                if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f')))
                    return false;
            }
            return true;
        }
    }
}
