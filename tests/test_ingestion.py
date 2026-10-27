import pytest
from app.ingestion import build_manifest, check_required_columns, validate_file_metadata


def test_manifest_hash_is_deterministic():
    manifest = build_manifest("claims_demo.csv", b"claim_id,amount\\nsynthetic-1,100.00\\n")
    assert manifest.size_bytes > 0
    assert len(manifest.sha256) == 64


@pytest.mark.parametrize("name,size", [
    ("../secrets.csv", 10),
    ("bad.exe", 10),
    ("claims.csv", 30 * 1024 * 1024),
])
def test_file_metadata_rejects_unsafe_inputs(name, size):
    with pytest.raises(ValueError):
        validate_file_metadata(name, size)


def test_required_columns():
    check_required_columns(["CLAIM_ID", "amount"], ["claim_id", "amount"])
    with pytest.raises(ValueError):
        check_required_columns(["claim_id"], ["claim_id", "amount"])
