
set -euo pipefail

IMAGE="${APPTAINER_IMAGE:-/projects/bekz/yzhao25/ts-gh200.sif}"
HF_BIND="${HF_BIND:-/work/nvme/bekz/yzhao25/huggingface:/mnt/huggingface}"


apptainer exec --nv \
  --bind /opt/nvidia:/opt/nvidia \
  --bind "${HF_BIND}" \
  "${IMAGE}" \
  bash gh200/serve_qwen3_moe.sh 