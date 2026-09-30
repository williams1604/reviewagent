from reviewagent.core.finding import Finding, Severity


def test_finding_creation():
    finding = Finding(
        severity=Severity.HIGH,
        category="security",
        message="Hardcoded API key detected.",
        file="sample_test.py",
        line_number=12,
        explanation="Storing plaintext secrets in source code is unsafe.",
        recommendation="Use environment variables instead.",
        suggested_fix="API_KEY = os.getenv('API_KEY')"
    )

    assert finding.severity == Severity.HIGH
    assert finding.category == "security"
    assert finding.line_number == 12
    assert finding.file == "sample_test.py"


def test_finding_to_dict_and_from_dict():
    finding = Finding(
        severity=Severity.CRITICAL,
        category="bug",
        message="ZeroDivisionError risk",
        file="calc.py",
        line_number=25
    )

    data = finding.to_dict()
    assert data["severity"] == "CRITICAL"
    assert data["category"] == "bug"
    assert data["file"] == "calc.py"

    reconstructed = Finding.from_dict(data)
    assert reconstructed.severity == Severity.CRITICAL
    assert reconstructed.line_number == 25


def test_severity_from_str():
    assert Severity.from_str("critical") == Severity.CRITICAL
    assert Severity.from_str("high") == Severity.HIGH
    assert Severity.from_str("medium") == Severity.MEDIUM
    assert Severity.from_str("low") == Severity.LOW
    assert Severity.from_str("info") == Severity.INFO
    assert Severity.from_str("unknown_val") == Severity.LOW
