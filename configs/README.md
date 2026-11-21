There are three defined configs:
- sem-eval-all-langs, which runs it on a combined dataset of all four tracks. Command: `uv run machamp-nlp/train.py --dataset_configs configs/sem-eval-all-langs.json  --parameters_config params.json`
- sem-eval-all-langs-multitask, which runs it on a combined dataset of all four tracks but with each task treated as a seperate task rather than combined. Command: `uv run machamp-nlp/train.py --dataset_configs configs/sem-eval-all-langs-multitask.json  --parameters_confi
g params.json`
- sem-eval-english-two-stage, which runs it first on the english track and then on the multi track, in both cases using the english dev set. Make sure to use --sequential when running this one so that the second stage is run using the model trained on the first stage. Command: `uv run machamp-nlp/train.py --dataset_configs configs/sem-eval-english-two-stage.json  --parameters_config params.json --sequential`
