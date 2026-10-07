#!/usr/bin/env python3
import hashlib,json,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=json.loads((R/'BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1.json').read_text())
assert S['build_id']=='S1.42AK-BMDSFIX1-DIAG1PATH1'
assert S['base_profile']=='Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z'
assert S['base_sha256']=='31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e'
assert S['output_profile']=='Profiles/LC V1 S1.42AK-D1P1.r2z'
assert S['profile_name']=='LC V1 S1.42AK-D1P1'
for k in ('mod_state_changes','mod_additions','mod_removals','config_patches','file_injections','local_plugin_builds'): assert S[k]==[]
base=R/S['base_profile']; assert base.is_file()
h=hashlib.sha256(base.read_bytes()).hexdigest(); assert h==S['base_sha256'],(h,S['base_sha256'])
with zipfile.ZipFile(base) as z:
    exp=z.read('export.r2x').decode('utf-8-sig')
    assert 'profileName: LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector' in exp
    expected={
      'BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll':'3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1',
      'BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll':'f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92',
      'BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll':'901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06'}
    for p,e in expected.items(): assert hashlib.sha256(z.read(p)).hexdigest()==e
root=r'C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles'
old='LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector'; new=S['profile_name']
rels=[r'BepInEx\patchers\MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix\LCOfficeV81Preloader\LCOfficeV81Preloader.dll',r'BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll']
old_l=[len(root+'\\'+old+'\\'+x) for x in rels]; new_l=[len(root+'\\'+new+'\\'+x) for x in rels]
assert old_l==[260,262],old_l
assert max(new_l)<=220,new_l
state=json.loads((R/'Current/CURRENT_STATE.json').read_text())
assert state['accepted_baseline']['build_id']=='S1.42AK'
assert state['active_candidate']['build_id']=='S1.42AK-BMDSFIX1'
assert state['controllers']['runtime_active_build']=='S1.42AK-BMDSFIX1-DIAG1'
assert (R/'RuntimeInbox/ACTIVE_BUILD.txt').read_text().strip()=='S1.42AK-BMDSFIX1-DIAG1'
cur=json.loads((R/'BuildSpecs/current.json').read_text()); assert cur['enabled'] is False
print('DIAG1PATH1 source/static contract PASS; old paths',old_l,'new paths',new_l)
