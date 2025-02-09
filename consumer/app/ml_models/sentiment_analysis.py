from pysentimiento import create_analyzer

from app.utils.logger import get_logger

logger = get_logger(__name__)


class SentimentAnalysisModel:
    def __init__(self):
        """Inicializa a instância responsável por classificar as avaliações"""
        logger.info("Initiating the analyzer")
        self.analyzer = create_analyzer(task="sentiment", lang="pt")

    def predict(self, sentence):
        """Prediz o sentimento de uma sentença.

        Args:
            sentence: Texto a ser classificado.

        Returns:
            str: Classificação do sentimento, exemplo: 'POS', 'NEG' ou 'NEU'.
        """
        return self.analyzer.predict(sentence)


analyzer = SentimentAnalysisModel()
