import csv
import pandas as pd

SWAP = {"FORWARD_ENTAILMENT": "BACKWARD_ENTAILMENT",
        "BACKWARD_ENTAILMENT": "FORWARD_ENTAILMENT"}

# column positions in the official files (counting from 0)
INSTANCE_ID, LABEL = 0, 6


def add_partner_columns(in_path, out_path, offset=0):
    """Appends two columns to a TSV: instance_idx and partner_idx.

    The partner of a row is the row with the same instance_id, but with
    '__original' swapped for '__flipped' (or the other way around).
    Rows without a partner (the NEGATIVE_OTHER rows) get -1.

    offset: added to all indices. Use a different offset per file, so that
    indices of different files never collide when they share one MaChAmp task.
    """
    df = pd.read_csv(in_path, sep="\t", dtype=str, keep_default_na=False,
                     quoting=csv.QUOTE_NONE)
    ids = df.iloc[:, INSTANCE_ID].tolist()
    labels = df.iloc[:, LABEL].tolist()

    # find, for every row, the row of its original/flipped counterpart
    index = {iid: i for i, iid in enumerate(ids)}
    partner = []
    for iid in ids:
        if iid.endswith("__original"):
            other = iid[: -len("__original")] + "__flipped"
        elif iid.endswith("__flipped"):
            other = iid[: -len("__flipped")] + "__original"
        else:
            other = None
        partner.append(index.get(other, -1))

    # sanity checks, printed below
    n = len(df)
    no_partner = sum(p == -1 for p in partner)
    asym = sum(1 for i, p in enumerate(partner) if p != -1 and partner[p] != i)
    bad = sum(1 for i, p in enumerate(partner)
              if p != -1 and SWAP.get(labels[i], labels[i]) != labels[p])
    print(f"{in_path}: {n} rows, {no_partner} without partner, "
          f"{asym} asymmetric, {bad} with non-matching reversed label")
    if no_partner:
        missing = pd.Series([labels[i] for i, p in enumerate(partner) if p == -1])
        print("rows without partner, by label:")
        print(missing.value_counts().to_string())

    df["instance_idx"] = [i + offset for i in range(n)]
    df["partner_idx"] = [(p + offset) if p != -1 else -1 for p in partner]
    df.to_csv(out_path, sep="\t", index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("new columns are at indices",
          df.columns.get_loc("instance_idx"), "and", df.columns.get_loc("partner_idx"))