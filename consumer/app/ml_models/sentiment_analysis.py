from transformers import pipeline

from app.utils.logger import get_logger

logger = get_logger(__name__)


class SentimentAnalysisModel:
    def __init__(self):
        """Inicializa a instância responsável por classificar as avaliações"""
        logger.info("Initiating the analyzer")
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="pysentimiento/robertuito-sentiment-analysis",
            device=0,
        )

    def predict(self, sentence: str | list):
        """Prediz o sentimento de uma sentença.

        Args:
            sentence: Texto a ser classificado.

        Returns:
            str: Classificação do sentimento, exemplo: 'POS', 'NEG' ou 'NEU'.
        """
        return self.analyzer(sentence, return_all_scores=True)


_analyzer_instance = None


def get_analyzer():
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = SentimentAnalysisModel()
    return _analyzer_instance
