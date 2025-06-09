from utils.val_metrics import compute_metrics
import os

test_order = 'unpaired'

metrics = compute_metrics(
    os.path.join(f"/home/ugrp/ladi-vton/out_2_{test_order}"),
    test_order,
    'vitonhd', 'all', ['all'], "args.dresscode_dataroot", "/home/ugrp/ladi-vton/vtonHD")

print(metrics, flush=True)