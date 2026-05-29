# exclusively for GH200
CACHE_ROOT="/tmp/${USER_NAME}-cache"
mkdir -p "$CACHE_ROOT/triton" "$CACHE_ROOT/torchinductor" "$CACHE_ROOT/xdg"
export XDG_CACHE_HOME="$CACHE_ROOT/xdg"
export TRITON_CACHE_DIR="$CACHE_ROOT/triton"
export TORCHINDUCTOR_CACHE_DIR="$CACHE_ROOT/torchinductor"
export LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_aarch64/25.5/cuda/12.9/lib64:$LD_LIBRARY_PATH

export CC="${CC:-/usr/bin/cc}"
if [[ -z "${CXX:-}" || "${CXX}" == "CC" ]]; then
  export CXX="/usr/bin/g++"
fi

tokenspeed serve Qwen/Qwen3-32B \
   --host 0.0.0.0 \
   --port 8003 \
   --tensor-parallel-size 4 \
   --max-total-tokens 16384