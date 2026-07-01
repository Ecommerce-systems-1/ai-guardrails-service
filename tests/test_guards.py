from src.guards.pii import PIIGuard


def test_pii_email_triggers():
    result = PIIGuard().check_input("My email is john@gmail.com please help")
    assert result.triggered is True
    assert result.severity == "BLOCK"
    assert any("email" in v for v in result.violations)


def test_pii_email_masked_in_violation():
    result = PIIGuard().check_input("contact me at alice@example.org")
    assert any("***@example.org" in v for v in result.violations)


def test_pii_credit_card_luhn_valid_triggers():
    # 4111-1111-1111-1111 is a valid Luhn test card
    result = PIIGuard().check_input("charge 4111-1111-1111-1111 to my order")
    assert result.triggered is True
    assert any("credit card" in v for v in result.violations)


def test_pii_credit_card_luhn_invalid_passes():
    # 4111-1111-1111-1112 fails Luhn check — should not trigger
    result = PIIGuard().check_input("reference number 4111-1111-1111-1112")
    assert result.triggered is False


def test_pii_ssn_triggers():
    result = PIIGuard().check_input("SSN is 123-45-6789")
    assert result.triggered is True
    assert any("SSN" in v for v in result.violations)


def test_pii_clean_text_passes():
    result = PIIGuard().check_input("I am looking for a winter coat in size medium")
    assert result.triggered is False
    assert result.severity == "PASS"
