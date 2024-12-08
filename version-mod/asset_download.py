import os
import subprocess
from zipfile import ZipFile


def download_asset_bundle(res_version, asset_bundle_name):
    if os.path.exists(f"{res_version}/{asset_bundle_name}"):
        return
    os.makedirs(res_version, exist_ok=True)
    subprocess.run(
        [
            "curl", "-L", "-O", "-g",
            "--output-dir", res_version,
            f"https://ak.hycdn.cn/assetbundle/official/Android/assets/{
                res_version}/{asset_bundle_name}"
        ]
    )
    with ZipFile(f"{res_version}/{asset_bundle_name}") as f:
        f.extractall(res_version)
