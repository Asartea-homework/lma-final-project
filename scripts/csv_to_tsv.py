import pandas as pd
import pathlib

DATA_PATH = pathlib.Path(__file__).parent.parent / "final-data"
print(f"Converting CSV files in {DATA_PATH} to TSV...")
TRAIN_DATA = DATA_PATH / "train"
DEV_DATA = DATA_PATH / "dev"
for file in TRAIN_DATA.glob("*.csv"):
    print(f"Converting {file} to TSV...")
    df = pd.read_csv(file)
    df.to_csv(file.with_suffix(".tsv"), sep="\t", index=False)

for file in DEV_DATA.glob("*.csv"):
    print(f"Converting {file} to TSV...")
    df = pd.read_csv(file)
    df.to_csv(file.with_suffix(".tsv"), sep="\t", index=False)
