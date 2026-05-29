#!/bin/bash

set -euo pipefail

IMAGE="${APPTAINER_IMAGE:-/projects/bekz/yzhao25/ts-gh200.sif}"
HF_BIND="${HF_BIND:-/work/nvme/bekz/yzhao25/huggingface:/mnt/huggingface}"


exec apptainer exec --nv --bind "${HF_BIND}" \
                         --bind /opt/nvidia:/opt/nvidia \
                        "${IMAGE}" \
                        /bin/bash --login
