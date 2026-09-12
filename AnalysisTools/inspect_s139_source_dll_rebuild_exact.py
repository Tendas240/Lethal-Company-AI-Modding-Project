#!/usr/bin/env python3
import argparse, hashlib, json, os, shutil, subprocess, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE="af415c8d6fdb69b0b7c88102e714764f3dc24b57"
BUILD="fdb6b94e34144f860f6ac6eb2fd5bdbdd7797ef5"
RUN=34141360051
SDK="10.0.400"
ILSPY="11.0.0.9375"
SRC="Patches/S139CompatibilityFixes/Plugin.cs"
PROJ="Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj"
PDIR="Patches/S139CompatibilityFixes"
DLL=f"{PDIR}/bin/Release/netstandard2.1/S139CompatibilityFixes.dll"
MEMBER="BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"
SRC_SHA="2b8a326383ea5f39a69f7b370836180509dc5a34ec0c1b98dbe0734f4f87707d"
PROJ_SHA="c51a47a8eb502df7a787c2a08ed90962e284fa68e4557c8bc022bc56e68dd39b"
DLL_SHA="bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573"
AH=("Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z","06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e")
AI=("Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z","d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2")
INPUTS={"Directory.Build.props","Directory.Build.targets","Directory.Packages.props","global.json"}
PROPS="TargetFramework,LangVersion,Optimize,DebugType,DebugSymbols,Deterministic,Nullable,ImplicitUsings,DefineConstants,PathMap,ContinuousIntegrationBuild,SourceRevisionId,InformationalVersion,AssemblyVersion,FileVersion,Version,VersionSuffix,TreatWarningsAsErrors,WarningLevel"

def H(b): return hashlib.sha256(b).hexdigest()
def R(cmd,cwd=ROOT): return subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
def OK(p,label):
    if p.returncode: raise RuntimeError(f"{label} failed ({p.returncode})\n{p.stdout}\n{p.stderr}")
    return p.stdout
def SHOW(c,p):
    q=subprocess.run(["git","show",f"{c}:{p}"],cwd=ROOT,capture_output=True)
    if q.returncode: raise RuntimeError(q.stderr.decode(errors="replace"))
    return q.stdout
def TREE(c):
    xs=OK(R(["git","ls-tree","-r","--name-only",c]),f"tree {c}").splitlines()
    return sorted(x for x in xs if Path(x).name in INPUTS)
def EXTRACT(profile,psha,dst):
    p=ROOT/profile
    if H(p.read_bytes())!=psha: raise RuntimeError(f"profile SHA mismatch: {profile}")
    with zipfile.ZipFile(p) as z:
        d=z.read(MEMBER)
    if H(d)!=DLL_SHA: raise RuntimeError(f"runtime DLL SHA mismatch: {profile}")
    dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(d)
def DECOMP(tool,dll,il=False):
    return OK(R([str(tool)]+(["--ilcode"] if il else [])+[str(dll)]),"ILSpy").replace("\r\n","\n").replace("\r","\n")
def COPY(src,dst):
    if not src.exists(): return None
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
    return {"sha256":H(src.read_bytes()),"size":src.stat().st_size}
def CSC(text):
    needles=("Task \"Csc\"","CommandLineArguments","CscTool","csc.dll","langversion","define:","deterministic","pathmap","debug:","optimize","nullable","reference:","analyzer:")
    return "\n".join(x for x in text.splitlines() if any(n.lower() in x.lower() for n in needles))+"\n"
def ASSETS(p):
    d=json.loads(p.read_text())
    tk=next(iter(d.get("targets",{})),None); t=d.get("targets",{}).get(tk,{})
    return {"target":tk,"libraries":sorted(d.get("libraries",{})),
            "compile":sorted(f"{k}:{x}" for k,v in t.items() for x in v.get("compile",{})),
            "runtime":sorted(f"{k}:{x}" for k,v in t.items() for x in v.get("runtime",{})),
            "packageFolders":sorted(d.get("packageFolders",{})),
            "frameworks":d.get("project",{}).get("frameworks",{})}
def SUMMARY(out,v):
    c=v.get("comparison",{}); e=v.get("effective",{})
    out.joinpath("SUMMARY.md").write_text(f"""# S139 Effective-Build-Input Review
- Status: `{v.get('status')}`
- Historical build run: `{RUN}`
- Historical pre-build: `{PRE}`
- Historical build commit: `{BUILD}`
- Historical runner: `ubuntu-24.04 / 20260831.293.1`
- Historical image highest installed SDK: `10.0.400`
- setup-dotnet request: `8.0.x` (reported installed `8.0.424`)
- Reproduction SDK: `{e.get('selected_sdk','<none>')}`
- Runtime SHA: `{DLL_SHA}`
- Rebuild SHA: `{c.get('rebuilt_sha256','<none>')}`
- Byte identical: `{c.get('byte_identical',False)}`
- C# identical: `{c.get('csharp_identical',False)}`
- IL identical: `{c.get('il_identical',False)}`

No tracked global.json/Directory.Build.props/Directory.Build.targets/Directory.Packages.props existed in the historical tree.
The historical setup-dotnet action installed 8.0.x into the shared dotnet root but did not create an SDK selector.
This analysis therefore tests 10.0.400, the highest SDK present on the exact historical runner image, while capturing restore/MSBuild/Csc inputs.

Analysis-Evidence only: no DIAG1 build, controller change, runtime test, or canonical provenance closure is authorized.
""",encoding="utf-8")

def main():
    a=argparse.ArgumentParser(); a.add_argument("--output-dir",type=Path,required=True); a.add_argument("--ilspy",type=Path,required=True)
    n=a.parse_args(); out=n.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    tool=n.ilspy.resolve() if n.ilspy.is_absolute() else (ROOT/n.ilspy).resolve()
    wt=out.parent/"s139-historical-prebuild-worktree"; v={"schema_version":4,"status":"RUNNING","historical_run":RUN}; rc=1
    try:
        v["analysis_head"]=OK(R(["git","rev-parse","HEAD"]),"head").strip(); v["github_run_id"]=os.getenv("GITHUB_RUN_ID")
        for label,data,exp in [
            ("current source",(ROOT/SRC).read_bytes(),SRC_SHA),("pre source",SHOW(PRE,SRC),SRC_SHA),("build source",SHOW(BUILD,SRC),SRC_SHA),
            ("current project",(ROOT/PROJ).read_bytes(),PROJ_SHA),("pre project",SHOW(PRE,PROJ),PROJ_SHA),("build project",SHOW(BUILD,PROJ),PROJ_SHA)]:
            if H(data)!=exp: raise RuntimeError(f"{label} SHA mismatch")
        ri={"pre":TREE(PRE),"build":TREE(BUILD)}
        if ri["pre"] or ri["build"]: raise RuntimeError(f"unexpected historical repo build inputs: {ri}")
        v["repo_wide_inputs"]=ri
        wf=SHOW(PRE,".github/workflows/atomic-build-s142ah-v8-final.yml").decode()
        pb=SHOW(PRE,"BuildSystem/profile_builder.py").decode()
        if 'dotnet-version: "8.0.x"' not in wf or 'subprocess.run(["dotnet", "build", str(project), "-c", config], check=True)' not in pb:
            raise RuntimeError("historical build contract mismatch")
        ref=out/"reference"; rb=out/"rebuilt"; ah=ref/"S1.42AH/S139CompatibilityFixes.dll"; ai=ref/"S1.42AI/S139CompatibilityFixes.dll"
        EXTRACT(*AH,ah); EXTRACT(*AI,ai)
        if ah.read_bytes()!=ai.read_bytes(): raise RuntimeError("AH/AI runtime DLL mismatch")
        out.joinpath("HOST_DOTNET_SDKS.txt").write_text(OK(R(["dotnet","--list-sdks"]),"list sdks"))
        if wt.exists(): subprocess.run(["git","worktree","remove","--force",str(wt)],cwd=ROOT,capture_output=True)
        OK(R(["git","worktree","add","--detach",str(wt),PRE]),"worktree")
        if (wt/"global.json").exists(): raise RuntimeError("historical global.json unexpectedly exists")
        unpinned=OK(R(["dotnet","--version"],wt),"unpinned sdk").strip()
        selector={"sdk":{"version":SDK,"rollForward":"disable","allowPrerelease":False}}
        sb=(json.dumps(selector,indent=2)+"\n").encode(); (wt/"global.json").write_bytes(sb)
        selected=OK(R(["dotnet","--version"],wt),"selected sdk").strip()
        if selected!=SDK: raise RuntimeError(f"expected SDK {SDK}, got {selected}")
        v["effective"]={"current_runner_unpinned_sdk":unpinned,"selected_sdk":selected,"selector_sha256":H(sb),"selector_tracked":False}
        out.joinpath("DOTNET_INFO.txt").write_text(OK(R(["dotnet","--info"],wt),"dotnet info"))
        shutil.rmtree(wt/PDIR/"bin",ignore_errors=True); shutil.rmtree(wt/PDIR/"obj",ignore_errors=True)
        b=R(["dotnet","build",PROJ,"-c","Release","-v:diag"],wt)
        out.joinpath("BUILD_DIAGNOSTIC.txt").write_text(b.stdout); out.joinpath("BUILD_STDERR.txt").write_text(b.stderr); out.joinpath("CSC_RELEVANT_LINES.txt").write_text(CSC(b.stdout))
        OK(b,"effective build")
        mp=R(["dotnet","msbuild",PROJ,"-nologo","-p:Configuration=Release",f"-getProperty:{PROPS}"],wt)
        out.joinpath("MSBUILD_EFFECTIVE_PROPERTIES.txt").write_text(mp.stdout+("\nSTDERR:\n"+mp.stderr if mp.stderr else "")); OK(mp,"msbuild property query")
        obj=wt/PDIR/"obj"; restore={}
        for rel in ("project.assets.json","S139CompatibilityFixes.csproj.nuget.g.props","S139CompatibilityFixes.csproj.nuget.g.targets","S139CompatibilityFixes.csproj.nuget.dgspec.json"):
            r=COPY(obj/rel,out/"restore"/rel)
            if r: restore[rel]=r
        if "project.assets.json" not in restore: raise RuntimeError("project.assets.json missing")
        v["restore_files"]=restore; v["package_resolution"]=ASSETS(obj/"project.assets.json")
        out.joinpath("PACKAGE_RESOLUTION.json").write_text(json.dumps(v["package_resolution"],indent=2)+"\n")
        built=wt/DLL
        if not built.exists(): raise RuntimeError("rebuilt DLL missing")
        rd=rb/"S139CompatibilityFixes.dll"; rd.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(built,rd)
        ver=OK(R([str(tool),"--version"]),"ilspy version")
        if ILSPY not in ver: raise RuntimeError(f"ILSpy mismatch: {ver.strip()}")
        rcs, bcs, ril, bil=DECOMP(tool,ai),DECOMP(tool,rd),DECOMP(tool,ai,True),DECOMP(tool,rd,True)
        ref.joinpath("S1.42AI/FULL_CSHARP.txt").write_text(rcs); ref.joinpath("S1.42AI/FULL_IL.txt").write_text(ril)
        rb.joinpath("FULL_CSHARP.txt").write_text(bcs); rb.joinpath("FULL_IL.txt").write_text(bil)
        x,y=ai.read_bytes(),rd.read_bytes()
        v["comparison"]={"runtime_sha256":H(x),"rebuilt_sha256":H(y),"runtime_size":len(x),"rebuilt_size":len(y),
                         "byte_identical":x==y,"csharp_identical":rcs==bcs,"il_identical":ril==bil,
                         "runtime_il_sha256":H(ril.encode()),"rebuilt_il_sha256":H(bil.encode())}
        if x==y: v["status"]="PASS_EFFECTIVE_SDK_CANDIDATE_BYTE_IDENTICAL"; v["source_to_dll_provenance"]="ANALYSIS_CAUSE_IDENTIFIED_NOT_CANONICALIZED"; rc=0
        else: v["status"]="FAIL_EFFECTIVE_SDK_CANDIDATE_NOT_BYTE_IDENTICAL"; v["source_to_dll_provenance"]="OPEN_REVIEW_REQUIRED"; rc=2
    except Exception as e:
        v["status"]="FAIL_ANALYSIS_ERROR"; v["source_to_dll_provenance"]="OPEN_ANALYSIS_ERROR"; v["error"]=f"{type(e).__name__}: {e}"; rc=1
    finally:
        subprocess.run(["git","worktree","remove","--force",str(wt)],cwd=ROOT,capture_output=True); subprocess.run(["git","worktree","prune"],cwd=ROOT,capture_output=True); shutil.rmtree(wt,ignore_errors=True)
        out.joinpath("VERIFICATION.json").write_text(json.dumps(v,indent=2)+"\n"); SUMMARY(out,v)
    print(json.dumps({"status":v["status"],"effective":v.get("effective"),"comparison":v.get("comparison")},indent=2)); return rc
if __name__=="__main__": raise SystemExit(main())
