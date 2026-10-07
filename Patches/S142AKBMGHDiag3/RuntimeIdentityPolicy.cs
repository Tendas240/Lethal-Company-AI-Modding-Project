using System;

namespace S142AKBMGHDiag3
{
    // Pure structural identity checks for the loaded runtime target.
    internal static class RuntimeIdentityPolicy
    {
        internal static void ValidateAssemblyIdentity(
            string typeFullName,
            string assemblySimpleName,
            bool assemblyIsDynamic)
        {
            if (typeFullName != "EntranceTeleport")
                throw new InvalidOperationException("EntranceTeleport runtime type identity mismatch.");
            if (assemblySimpleName != "Assembly-CSharp")
                throw new InvalidOperationException("EntranceTeleport declaring assembly name mismatch.");
            if (assemblyIsDynamic)
                throw new InvalidOperationException("EntranceTeleport declaring assembly is dynamic.");
        }

        internal static void ValidateTeleportMethodIdentity(
            bool isPublic,
            bool isStatic,
            int parameterCount,
            string returnTypeFullName,
            bool hasBody)
        {
            if (!isPublic || isStatic || parameterCount != 0 || returnTypeFullName != "System.Void" || !hasBody)
                throw new InvalidOperationException("Exact installed-V81 EntranceTeleport.TeleportPlayer() contract/body mismatch.");
        }
    }
}
