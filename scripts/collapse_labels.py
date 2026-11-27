import pandas as pd
import pathlib


def collapse_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse the labels in the dataframe to two classes: ENTAILMENT and NOT_ENTAILMENT.
    """
    df.iloc[:, 5] = df.iloc[:, 5].apply(
        lambda x: (
            "ENTAILMENT"
            if x in ["FORWARD_ENTAILMENT", "BACKWARD_ENTAILMENT"]
            else "NOT_ENTAILMENT"
        )
    )
    return df


DATA_PATH = pathlib.Path(__file__).parent.parent / "final-data"
print(f"Collapsing labels in {DATA_PATH}...")
TRAIN_DATA = DATA_PATH / "train"
DEV_DATA = DATA_PATH / "dev"
for file in TRAIN_DATA.glob("dico_nli_train_track[1-4]_participant_labeled.tsv"):
    print(f"Collapsing labels in {file}")
    df = pd.read_csv(file, sep="\t")
    df = collapse_labels(df)
    df.to_csv(
        file.with_name(file.stem + "_collapsed").with_suffix(".tsv"),
        sep="\t",
        index=False,
        header=False,
    )

for file in DEV_DATA.glob("dico_nli_dev_track[1-4]_participant_labeled.tsv"):
    print(f"Collapsing labels in {file}")
    df = pd.read_csv(file, sep="\t")
    df = collapse_labels(df)
    df.to_csv(
        file.with_name(file.stem + "_collapsed").with_suffix(".tsv"),
        sep="\t",
        index=False,
        header=False,
    )
