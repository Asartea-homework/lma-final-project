# Setup

Create venv:

```bash
uv venv
```

Activate venv:

```bash
source .venv/bin/activate
```

Sync packages:

```bash
uv sync
```

# Running

## Configs

Sem-eval-all-langs runs the combined dataset of all four tracks:

```bash
uv run machamp-nlp/train.py --dataset_configs configs/sem-eval-all-langs.json  --parameters_config params.json
```

Sem-eval-all-langs-multitask runs the combined dataset of all four tracks but with each task treated as a separate task rather than combined:

```bash
uv run machamp-nlp/train.py --dataset_configs configs/sem-eval-all-langs
-multitask.json  --parameters_config params.json
```

Sem-eval-english-two-stage runs it first on the English track and then on the multi track, in both cases using the English dev set. Make sure to use --sequential when running this one so that the second stage is run using the model trained on the first stage:

```bash
uv run machamp-nlp/train.py --dataset_configs configs/sem-eval-english-two-stage-stage-one.json configs/sem-eval-english-two-stage-stage-two.json --parameters_config params.json --sequential
```
