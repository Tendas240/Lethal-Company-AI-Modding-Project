#!/usr/bin/env python3
"""Persist the exact completed discovery artifact on this analysis branch only."""
import hashlib, io, json, os, urllib.request, urllib.parse, zipfile
REPO = "Tendas240/Lethal-Company-AI-Modding-Project"
BRANCH = "analysis/s142ai-native-spawn-owners"
ARTIFACT = 10268522778
RUN = 34611826588
SOURCE = "71973b25c395cef4d0022a0054975cdab44e37d2"
DIGEST = "40d5c51d3211f8a31388e91592ca08d07c61a9a792247307f90a14b10b660e06"
DIRECTORY = "SourceEvidence/NativeSpawnOwners/20260911T144505Z"
if os.environ["GITHUB_REPOSITORY"] != REPO or os.environ["GITHUB_REF"] != "refs/heads/" + BRANCH:
    raise RuntimeError("Analysis publication branch/repository mismatch")
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None and urllib.parse.urlparse(newurl).hostname != "api.github.com":
            redirected.remove_header("Authorization")
        return redirected
opener = urllib.request.build_opener(SafeRedirect())
def api(endpoint, body=None, method=None, raw=False):
    request = urllib.request.Request("https://api.github.com/repos/" + REPO + "/" + endpoint,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json"},
        method=method or ("GET" if body is None else "POST"))
    with opener.open(request, timeout=120) as response:
        data = response.read()
    return data if raw else json.loads(data)
artifact = api(f"actions/artifacts/{ARTIFACT}")
if artifact["expired"] or artifact["workflow_run"]["id"] != RUN or artifact["workflow_run"]["head_sha"] != SOURCE:
    raise RuntimeError("Artifact provenance mismatch")
raw = api(f"actions/artifacts/{ARTIFACT}/zip", raw=True)
if hashlib.sha256(raw).hexdigest() != DIGEST:
    raise RuntimeError("Artifact archive digest mismatch")
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    names = z.namelist()
    if len(names) != len(set(names)) or len(names) != 13 or any("/" in n or "\\" in n or not n.endswith(".json") for n in names):
        raise RuntimeError("Unexpected artifact entry inventory")
    data = {n: z.read(n) for n in names}
manifest = json.loads(data["MANIFEST.json"])
if manifest["repository_commit"] != SOURCE or len(manifest["packages"]) != 7:
    raise RuntimeError("Discovery manifest mismatch")
if set(data) != {"MANIFEST.json"} | {r["file"] for r in manifest["reports"]}:
    raise RuntimeError("Manifest file inventory mismatch")
for record in manifest["reports"]:
    b = data[record["file"]]
    if hashlib.sha256(b).hexdigest() != record["sha256"] or len(b) != record["bytes"]:
        raise RuntimeError("Report byte verification failed")
parent = os.environ["GITHUB_SHA"]
if api("git/ref/heads/" + BRANCH)["object"]["sha"] != parent:
    raise RuntimeError("Analysis branch moved; refusing publication")
commit = api("git/commits/" + parent)
entries = [{"path": DIRECTORY + "/" + name, "mode": "100644", "type": "blob",
            "content": content.decode("utf-8")} for name, content in data.items()]
index = {"schema_version": 1, "run": RUN, "analysis_commit": SOURCE, "artifact_id": ARTIFACT,
         "artifact_zip_sha256": DIGEST, "publication_parent": parent,
         "files": [{"file": n, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
                   for n, b in sorted(data.items())]}
entries.append({"path": DIRECTORY + "/CAPTURE_INDEX.json", "mode": "100644", "type": "blob",
                "content": json.dumps(index, indent=2) + "\n"})
tree = api("git/trees", {"base_tree": commit["tree"]["sha"], "tree": entries})
new_commit = api("git/commits", {"message": "Preserve verified seven-package spawn-owner discovery artifact",
    "tree": tree["sha"], "parents": [parent]})
api("git/refs/heads/" + BRANCH, {"sha": new_commit["sha"], "force": False}, method="PATCH")
print(json.dumps({"commit": new_commit["sha"], "directory": DIRECTORY, "verified_files": len(data)}, indent=2))
