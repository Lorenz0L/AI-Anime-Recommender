class AniMindException(Exception):
    pass

class DataFetchError(AniMindException):
    pass

class VectorStoreError(AniMindException):
    pass

class RecommendationError(AniMindException):
    pass
