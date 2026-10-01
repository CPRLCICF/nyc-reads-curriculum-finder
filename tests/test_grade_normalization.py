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


def test_unavailable_curriculum_response_has_safe_rendering_contract(monkeypatch):
    monkeypatch.setattr(
        _shared,
        '_fetch_schools_csv',
        lambda: [{
            'school_name': 'J.H.S. 278 Marine Park',
            'district_#': '22',
            'grade': 'Middle Schools (6–8)',
            'grade_level': '6, 7, 8',
            'curriculum': 'N/A',
        }],
    )

    for grade in ['K', *[str(value) for value in range(1, 9)]]:
        response = _shared.build_search({
            'school': 'J.H.S. 278 Marine Park',
            'district': '22',
            'grade': grade,
        })

        assert response['message_type'] == 'curriculum_not_rolled_out'
        assert 'NYC Reads has not yet rolled out at this school.' in response['message']
        assert '<a ' not in response['message']
