import argparse
import os
import shutil

from cleanfid import fid
from tqdm import tqdm


def make_custom_stats(dresscode_dataroot: str, vitonhd_dataroot: str):
    if vitonhd_dataroot is not None:
        if not fid.test_stats_exists(f"vitonhd_all", mode='clean'):
            fid.make_custom_stats(f"vitonhd_all", os.path.join(vitonhd_dataroot, 'test', 'image'), mode="clean",
                                  verbose=True)
        if not fid.test_stats_exists(f"vitonhd_upper_body", mode='clean'):
            fid.make_custom_stats(f"vitonhd_upper_body", os.path.join(vitonhd_dataroot, 'test', 'image'), mode="clean",
                                  verbose=True)
