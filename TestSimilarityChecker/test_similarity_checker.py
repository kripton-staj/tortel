from tortel.extractor.crud import get_data
from tortel.similarity_checker.pipeline import (check_cosine_similarity,
                                                tokenization)

set_tokens = tokenization(get_data())
check_cosine_similarity(set_tokens)
