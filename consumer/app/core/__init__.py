def get_prediction(predictions):
    max_prediction = max(predictions, key=lambda x: x["score"])
    return max_prediction["label"]


def get_prediction_next(prediction, sentiment):
    return next(item["score"] for item in prediction if item["label"] == sentiment)


def format_sentiment_scores(prediction):
    return {
        "positive": round(get_prediction_next(prediction, "POS"), 3),
        "negative": round(get_prediction_next(prediction, "NEG"), 3),
        "neutral": round(get_prediction_next(prediction, "NEU"), 3),
    }
