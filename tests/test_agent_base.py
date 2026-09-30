from reviewagent.agents.base import BaseAgent, AgentResult
from reviewagent.core.finding import Finding, Severity


class DummyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DummyTestAgent",
            description="Dummy agent for base abstraction testing",
            supported_languages=["Python", "Java"]
        )

    def analyze(self, code_content: str, filename: str, severity: str = "LOW", refactor: bool = False) -> AgentResult:
        finding = Finding(
            severity=Severity.LOW,
            category="quality",
            message="Test message",
            file=filename
        )
        return AgentResult(
            agent_name=self.name,
            findings=[finding],
            raw_markdown="## Review Result",
            duration_seconds=0.05,
            issue_counts={"bugs": 0, "security": 0, "bad_practices": 1, "total": 1}
        )


def test_base_agent_interface():
    agent = DummyAgent()
    assert agent.name == "DummyTestAgent"
    assert agent.supports_language("Python") is True
    assert agent.supports_language("Java") is True
    assert agent.supports_language("Ruby") is False

    result = agent.analyze("print('test')", "test.py")
    assert result.agent_name == "DummyTestAgent"
    assert len(result.findings) == 1
    assert result.issue_counts["total"] == 1
