# chatgpt-gatherwool-cuttlefish
Gather the wool from the cuttlefish

## 使用方法

```bash
python cuttlefish.py -h  # help帮助
```

```bash
python cuttlefish.py --refresh --all  # 全量生成，默认每天上限200篇，强制刷新任务
python cuttlefish.py --refresh --n 0  # 指定类型，强制刷新任务
python cuttlefish.py --n 0            # 指定类型，读取已有的任务
```