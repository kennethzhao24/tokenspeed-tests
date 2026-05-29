# tokenspeed-tests
Simple test scripts for tokenspeed on GH200

- [ ] Multi-Node Test

## 1, Build container
```bash
apptainer build tokenspeed-gh200.sif container/ts-gh200-build.def
```

## 2. Launch a server with Qwen/Qwen3-30B-A3B
```bash
bash gh200/serve.sh
```

### 3. Benchmark server on ShareGPT dataset
```bash
bash gh200/bench.sh
```