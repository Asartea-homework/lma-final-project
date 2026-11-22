import torch


class HardCons:
    def __init__(self):
        self.str = "hardcons"
        self.metric_scores = {}
        self.pair_predictions = {}
        self.pair_golds = {}
        self.pair_map = {
            "EQUIVALENCE": "EQUIVALENCE",
            "FORWARD_ENTAILMENT": "BACKWARD_ENTAILMENT",
            "BACKWARD_ENTAILMENT": "FORWARD_ENTAILMENT",
            "NEGATIVE_OTHER": "NEGATIVE_OTHER",
        }

    def score(self, preds, golds, vocabulary, mask=None, full_data=None):
        if full_data is None:
            raise ValueError(
                "full_data is required for softcons metric, but was not provided."
            )
        preds = torch.flatten(preds)
        golds = torch.flatten(golds)
        if mask is not None:
            raise NotImplementedError(
                "Masking is not implemented for softcons metric. Please provide unmasked predictions and gold labels."
            )

        for i in range(len(full_data)):
            if i >= len(preds):
                break

            instance_data = full_data[i]
            instance_id = instance_data.get("instance_id", None)
            if instance_id is None:
                raise ValueError(
                    "Each instance in full_data must have an 'instance_id' key."
                )
            pair_id = instance_data.get("pair_id", None)
            if pair_id is None:
                raise ValueError(
                    "Each instance in full_data must have a 'pair_id' key."
                )
            direction = instance_id.split("__")[-1]

            pred = preds[i].item()
            pred_label = vocabulary[pred]
            gold = golds[i].item()
            gold_label = vocabulary[gold]

            if pair_id not in self.pair_predictions:
                self.pair_predictions[pair_id] = {}
                self.pair_golds[pair_id] = {}

            self.pair_predictions[pair_id][direction] = pred_label
            self.pair_golds[pair_id][direction] = gold_label

    def reset(self):
        self.pair_predictions = {}
        self.pair_golds = {}
        self.metric_scores = {}

    def get_score(self):
        total_pairs = 0
        consistent_and_correct_pairs = 0

        for pair_id, preds_dict in self.pair_predictions.items():
            if "flipped" in preds_dict and "original" in preds_dict:
                total_pairs += 1

                if (
                    self.pair_map.get(preds_dict["original"]) == preds_dict["flipped"]
                    and preds_dict["original"] == self.pair_golds[pair_id]["original"]
                    and preds_dict["flipped"] == self.pair_golds[pair_id]["flipped"]
                ):
                    consistent_and_correct_pairs += 1

        if total_pairs == 0:
            self.metric_scores[self.str] = 0.0
        else:
            self.metric_scores[self.str] = consistent_and_correct_pairs / total_pairs

        self.metrics_scores["sum"] = self.str
        return self.metric_scores

    def is_active(self):
        return len(self.pair_predictions) > 0 and len(self.pair_golds) > 0
