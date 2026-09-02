# Small unit tests for grade normalization and allowed_grades union logic
from api import _shared


def test_normalize_grade_tokens_union_contains_one():
    # descriptive (range/band) string that may not enumerate '1'
    descriptive = "Elementary Schools (PK–5/PK–8)"
    # explicit list that includes '1'
    explicit = "PK, 0K, 1, 2, 3, 4, 5"

    desc_tokens = set(_shared._normalize_grade_tokens(descriptive))
    exp_tokens = set(_shared._normalize_grade_tokens(explicit))

    allowed = desc_tokens.union(exp_tokens)

    # allowed_grades should include '1' when explicit fields are present
    assert '1' in allowed, f"expected '1' in allowed grades, got {allowed}"


def test_normalize_grade_tokens_basic_range():
    tokens = set(_shared._normalize_grade_tokens("K-2"))
    # ensure range parsing includes K and upper bound 2
    assert 'K' in tokens
    assert '2' in tokens
