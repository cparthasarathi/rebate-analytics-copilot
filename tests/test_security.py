import pytest
from app.security import detect_sensitive_markers, tokenize_identifier, validate_readonly_sql, validate_text

KEY = "local-demo-key-please-replace-32-bytes-minimum"


def test_validate_text_trims():
    assert validate_text("  hello  ") == "hello"


def test_validate_text_rejects_empty():
    with pytest.raises(ValueError):
        validate_text("  ")


def test_tokenization_is_stable_and_not_plain_identifier():
    token = tokenize_identifier("synthetic-person-123", KEY)
    assert token.startswith("tok_")
    assert "synthetic-person-123" not in token
    assert token == tokenize_identifier("synthetic-person-123", KEY)


def test_tokenization_requires_strong_secret():
    with pytest.raises(ValueError):
        tokenize_identifier("x", "short")


def test_sensitive_marker_heuristic():
    assert detect_sensitive_markers("patient_id=abc123")
    assert not detect_sensitive_markers("Show monthly rebate variance")


def test_sql_guard_allows_approved_select():
    sql = "SELECT period_month FROM GOLD.FACT_REBATE_TRANSACTION"
    assert validate_readonly_sql(sql, {"GOLD.FACT_REBATE_TRANSACTION"}) == sql


@pytest.mark.parametrize("sql", [
    "DELETE FROM GOLD.FACT_REBATE_TRANSACTION",
    "SELECT * FROM GOLD.FACT_REBATE_TRANSACTION; DROP TABLE X",
    "SELECT * FROM RESTRICTED_DATA.PATIENT_CROSSWALK",
    "SELECT * FROM GOLD.FACT_REBATE_TRANSACTION -- comment",
])
def test_sql_guard_rejects_unsafe_sql(sql):
    with pytest.raises(ValueError):
        validate_readonly_sql(sql, {"GOLD.FACT_REBATE_TRANSACTION"})
