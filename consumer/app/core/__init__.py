def get_prediction(predictions):
    max_prediction = max(predictions, key=lambda x: x["score"])
    return max_prediction["label"]


def get_prediction_next(prediction, sentiment):
    return next(item["score"] for item in prediction if item["label"] == sentiment)
