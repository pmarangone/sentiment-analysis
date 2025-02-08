from pysentimiento import create_analyzer

from app.utils.logger import get_logger

logger = get_logger(__name__)


class SentimentAnalysisModel:
    def __init__(self):
        logger.info("Initiating the analyzer")
        self.analyzer = create_analyzer(task="sentiment", lang="pt")

    def predict(self, sentence):
        model_output = self.analyzer.predict(sentence)
        print("model output", model_output)
        prediction = model_output.output
        return prediction


analyzer = SentimentAnalysisModel()
