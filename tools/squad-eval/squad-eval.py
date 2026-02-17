#!/usr/bin/env python3
"""
squad-eval — Evaluate squad agent performance

Evaluates agents based on their role (Research, Ops, Build):
- Research agents (Marcus/Galen): sources, citations, depth_score, business relevance
- Ops agents (Argus): uptime, health checks, alerts sent, response time
- Build agents (Archimedes): tools shipped, fixes deployed, tests run

Checks both learnings/ AND outputs/ directories for recent work.
"""

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: str  # research, ops, build
    host: str
    hostname: str
    workspace_path: str
    learnings_path: str
    outputs_path: str
    log_path: str


@dataclass
class EvaluationResult:
    """Evaluation result for a single agent."""
    agent_name: str
    role: str
    overall_score: float
    metrics: Dict[str, float]
    details: Dict[str, str]
    last_learning: Optional[str] = None
    last_output: Optional[str] = None
    uptime: str = "Unknown"
    status: str = "Unknown"


class SquadEvaluator:
    """Evaluates squad agents based on their role."""

    # Agent configurations
    AGENTS = {
        "marcus": AgentConfig(
            name="Marcus",
            role="research",
            host="100.98.223.103",
            hostname="marcus-squad",
            workspace_path="/home/exedev/.openclaw/workspace",
            learnings_path="/home/exedev/.openclaw/learnings",
            outputs_path="/home/exedev/.openclaw/workspace/outputs",
            log_path="journalctl --user -u openclaw --since '1 hour ago' --no-pager"
        ),
        "galen": AgentConfig(
            name="Galen",
            role="research",
            host="100.123.121.125",
            hostname="galen-squad",
            workspace_path="/home/exedev/.openclaw/workspace",
            learnings_path="/home/exedev/.openclaw/learnings",
            outputs_path="/home/exedev/.openclaw/workspace/outputs",
            log_path="journalctl --user -u openclaw --since '1 hour ago' --no-pager"
        ),
        "argus": AgentConfig(
            name="Argus",
            role="ops",
            host="100.108.219.91",
            hostname="argus-squad",
            workspace_path="/home/exedev/.openclaw/workspace",
            learnings_path="/home/exedev/.openclaw/learnings",
            outputs_path="/home/exedev/.openclaw/workspace/outputs",
            log_path="journalctl --user -u openclaw --since '1 hour ago' --no-pager"
        ),
        "archimedes": AgentConfig(
            name="Archimedes",
            role="build",
            host="100.100.56.102",
            hostname="archimedes-squad",
            workspace_path="/home/exedev/.openclaw/workspace",
            learnings_path="/home/exedev/.openclaw/learnings",
            outputs_path="/home/exedev/.openclaw/workspace/outputs",
            log_path="journalctl --user -u openclaw --since '1 hour ago' --no-pager"
        ),
    }

    def __init__(self):
        """Initialize evaluator."""
        self.local_workspace = Path.home() / ".openclaw/workspace"
        self.local_learnings = Path.home() / ".openclaw/learnings"

    def get_last_learning(self, agent: AgentConfig) -> Optional[Tuple[str, datetime]]:
        """Get last learning file and timestamp.

        Args:
            agent: Agent configuration

        Returns:
            (filename, timestamp) or None
        """
        # Check both learnings/ and outputs/
        for path_str in [agent.learnings_path, agent.outputs_path]:
            path = Path(path_str)
            if not path.exists():
                continue

            try:
                files = sorted(path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
                if files:
                    latest = files[0]
                    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                    return (latest.name, mtime)
            except Exception as e:
                pass

        return None

    def get_last_output(self, agent: AgentConfig) -> Optional[Tuple[str, datetime]]:
        """Get last output file and timestamp.

        Args:
            agent: Agent configuration

        Returns:
            (filename, timestamp) or None
        """
        # Check memory/ directory for daily summaries
        memory_path = Path(agent.workspace_path) / "memory"
        if memory_path.exists():
            try:
                files = sorted(memory_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
                if files:
                    latest = files[0]
                    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                    return (latest.name, mtime)
            except Exception:
                pass

        # Check outputs/ directory
        outputs_path = Path(agent.outputs_path)
        if outputs_path.exists():
            try:
                files = sorted(outputs_path.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
                if files:
                    latest = files[0]
                    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                    return (latest.name, mtime)
            except Exception:
                pass

        return None

    def evaluate_research_agent(self, agent: AgentConfig) -> EvaluationResult:
        """Evaluate a research agent (Marcus/Galen).

        Metrics:
        - Recent learning count (last 7 days)
        - Learning depth score (avg file size)
        - Sources/references cited
        - Business relevance score
        """
        metrics = {}
        details = {}

        # Get recent learnings
        last_week = datetime.now() - timedelta(days=7)
        recent_learnings = []

        learnings_path = Path(agent.learnings_path)
        if learnings_path.exists():
            for file in learnings_path.glob("*.md"):
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime > last_week:
                    recent_learnings.append(file)

        # Metric: Learning frequency
        metrics['learning_frequency'] = len(recent_learnings)
        details['recent_learnings'] = f"{len(recent_learnings)} in last 7 days"

        # Metric: Learning depth (avg file size)
        if recent_learnings:
            avg_size = sum(f.stat().st_size for f in recent_learnings) / len(recent_learnings)
            metrics['depth_score'] = avg_size / 1024  # KB
            details['avg_learning_size'] = f"{avg_size / 1024:.1f} KB"
        else:
            metrics['depth_score'] = 0
            details['avg_learning_size'] = "N/A"

        # Metric: Sources cited (heuristic)
        sources_count = 0
        for learning in recent_learnings:
            try:
                content = learning.read_text()
                sources_count += len(re.findall(r'https?://', content))
            except:
                pass
        metrics['sources_cited'] = sources_count
        details['sources'] = str(sources_count)

        # Metric: Business relevance (heuristic based on keywords)
        relevance_keywords = ['biopharma', 'ai', 'drug', 'clinical', 'trial', 'fda',
                          'openai', 'anthropic', 'claude', 'llm', 'agent']
        relevance_score = 0
        for learning in recent_learnings:
            try:
                content = learning.read_text().lower()
                relevance_score += sum(1 for kw in relevance_keywords if kw in content)
            except:
                pass
        metrics['business_relevance'] = relevance_score
        details['business_relevance'] = f"{relevance_score} keyword matches"

        # Calculate overall score
        # Normalize: max 14 learnings (2/day), 50KB depth, 20 sources, 10 relevance
        learning_score = min(metrics['learning_frequency'] / 14, 1.0) * 25
        depth_score = min(metrics['depth_score'] / 50, 1.0) * 25
        sources_score = min(metrics['sources_cited'] / 20, 1.0) * 25
        relevance_score = min(metrics['business_relevance'] / 10, 1.0) * 25

        overall_score = learning_score + depth_score + sources_score + relevance_score

        # Get last learning/output
        last_learning = self.get_last_learning(agent)
        last_output = self.get_last_output(agent)

        result = EvaluationResult(
            agent_name=agent.name,
            role=agent.role,
            overall_score=overall_score,
            metrics=metrics,
            details=details,
            last_learning=last_learning[0] if last_learning else None,
            last_output=last_output[0] if last_output else None,
            status="active" if last_learning and (datetime.now() - last_learning[1]).days < 2 else "inactive"
        )

        return result

    def evaluate_ops_agent(self, agent: AgentConfig) -> EvaluationResult:
        """Evaluate an ops agent (Argus).

        Metrics:
        - Uptime
        - Health checks performed
        - Alerts sent
        - Response time
        """
        metrics = {}
        details = {}

        # Get recent logs
        logs = subprocess.getoutput(f"ssh {agent.hostname} '{agent.log_path}'")

        # Metric: Health checks
        health_checks = logs.count("health") + logs.count("check")
        metrics['health_checks'] = health_checks
        details['health_checks'] = str(health_checks)

        # Metric: Alerts sent
        alerts = logs.count("alert") + logs.count("warning") + logs.count("error")
        metrics['alerts_sent'] = alerts
        details['alerts'] = str(alerts)

        # Metric: Uptime (from systemctl)
        try:
            status = subprocess.getoutput(f"ssh {agent.hostname} 'systemctl --user status openclaw --no-pager'")
            metrics['uptime_score'] = 1.0 if "active (running)" in status.lower() else 0.0
            details['service_status'] = "UP" if "active (running)" in status.lower() else "DOWN"
            uptime = "UP"
        except:
            metrics['uptime_score'] = 0.0
            details['service_status'] = "Unknown"
            uptime = "Unknown"

        # Metric: Response time (heuristic from log timestamps)
        # This is simplified - real implementation would track actual request times
        metrics['response_time'] = 1.0  # Placeholder
        details['response_time'] = "N/A"

        # Calculate overall score
        uptime_score = metrics['uptime_score'] * 40
        health_score = min(health_checks / 10, 1.0) * 20
        alert_score = min(alerts / 5, 1.0) * 20
        response_score = metrics['response_time'] * 20

        overall_score = uptime_score + health_score + alert_score + response_score

        # Get last learning/output
        last_learning = self.get_last_learning(agent)
        last_output = self.get_last_output(agent)

        result = EvaluationResult(
            agent_name=agent.name,
            role=agent.role,
            overall_score=overall_score,
            metrics=metrics,
            details=details,
            last_learning=last_learning[0] if last_learning else None,
            last_output=last_output[0] if last_output else None,
            uptime=uptime,
            status="active" if uptime == "UP" else "down"
        )

        return result

    def evaluate_build_agent(self, agent: AgentConfig) -> EvaluationResult:
        """Evaluate a build agent (Archimedes).

        Metrics:
        - Tools shipped
        - Fixes deployed
        - Tests run
        - Code quality
        """
        metrics = {}
        details = {}

        # Get tools directory
        tools_path = Path(agent.workspace_path) / "tools"
        tools_count = 0
        if tools_path.exists():
            tools_count = len([d for d in tools_path.iterdir() if d.is_dir()])

        # Metric: Tools shipped
        metrics['tools_shipped'] = tools_count
        details['tools'] = str(tools_count)

        # Metric: Fixes deployed (heuristic - check memory for deployment logs)
        memory_path = Path(agent.workspace_path) / "memory"
        fixes_deployed = 0
        if memory_path.exists():
            for file in memory_path.glob("*.md"):
                try:
                    content = file.read_text().lower()
                    fixes_deployed += content.count("fix") + content.count("deploy")
                except:
                    pass
        metrics['fixes_deployed'] = fixes_deployed
        details['fixes'] = str(fixes_deployed)

        # Metric: Tests run (heuristic)
        tests_run = 0
        if tools_path.exists():
            for tool_dir in tools_path.iterdir():
                if tool_dir.is_dir():
                    test_files = list(tool_dir.glob("test*.py")) + list(tool_dir.glob("*test*.py"))
                    tests_run += len(test_files)
        metrics['tests_run'] = tests_run
        details['tests'] = str(tests_run)

        # Metric: Code quality (heuristic - check for documentation)
        docs_count = 0
        if tools_path.exists():
            for tool_dir in tools_path.iterdir():
                if tool_dir.is_dir():
                    if (tool_dir / "README.md").exists():
                        docs_count += 1
        metrics['code_quality'] = docs_count / max(tools_count, 1) * 100
        details['documentation'] = f"{docs_count}/{tools_count} tools documented"

        # Calculate overall score
        # Normalize: max 50 tools, 20 fixes, 10 tests, 100% documentation
        tools_score = min(tools_count / 50, 1.0) * 25
        fixes_score = min(fixes_deployed / 20, 1.0) * 25
        tests_score = min(tests_run / 10, 1.0) * 25
        quality_score = metrics['code_quality'] / 100 * 25

        overall_score = tools_score + fixes_score + tests_score + quality_score

        # Get last learning/output
        last_learning = self.get_last_learning(agent)
        last_output = self.get_last_output(agent)

        result = EvaluationResult(
            agent_name=agent.name,
            role=agent.role,
            overall_score=overall_score,
            metrics=metrics,
            details=details,
            last_learning=last_learning[0] if last_learning else None,
            last_output=last_output[0] if last_output else None,
            status="active"
        )

        return result

    def evaluate(self, agent_id: str) -> EvaluationResult:
        """Evaluate a specific agent.

        Args:
            agent_id: Agent ID (marcus, galen, argus, archimedes)

        Returns:
            EvaluationResult
        """
        if agent_id not in self.AGENTS:
            raise ValueError(f"Unknown agent: {agent_id}")

        agent = self.AGENTS[agent_id]

        # Route to role-specific evaluation
        if agent.role == "research":
            return self.evaluate_research_agent(agent)
        elif agent.role == "ops":
            return self.evaluate_ops_agent(agent)
        elif agent.role == "build":
            return self.evaluate_build_agent(agent)
        else:
            raise ValueError(f"Unknown role: {agent.role}")

    def evaluate_all(self) -> List[EvaluationResult]:
        """Evaluate all agents.

        Returns:
            List of EvaluationResult objects
        """
        results = []
        for agent_id in self.AGENTS:
            try:
                result = self.evaluate(agent_id)
                results.append(result)
            except Exception as e:
                print(f"⚠️  Error evaluating {agent_id}: {e}")
        return results

    def print_result(self, result: EvaluationResult):
        """Print evaluation result.

        Args:
            result: EvaluationResult to print
        """
        status_emoji = "✅" if result.status == "active" else "❌"
        score_color = "🟢" if result.overall_score >= 75 else "🟡" if result.overall_score >= 50 else "🔴"

        print(f"\n{status_emoji} {result.agent_name} ({result.role.capitalize()})")
        print(f"   Score: {score_color} {result.overall_score:.1f}/100")
        print(f"   Status: {result.status.upper()}")
        print(f"   Last Learning: {result.last_learning or 'None'}")
        print(f"   Last Output: {result.last_output or 'None'}")

        # Role-specific metrics
        if result.role == "research":
            print(f"   📚 Recent Learnings: {result.details.get('recent_learnings', 'N/A')}")
            print(f"   📏 Avg Size: {result.details.get('avg_learning_size', 'N/A')}")
            print(f"   🔗 Sources: {result.details.get('sources', '0')}")
            print(f"   💼 Business Relevance: {result.details.get('business_relevance', '0')}")

        elif result.role == "ops":
            print(f"   🩺 Health Checks: {result.details.get('health_checks', '0')}")
            print(f"   🚨 Alerts: {result.details.get('alerts', '0')}")
            print(f"   📡 Service: {result.details.get('service_status', 'Unknown')}")

        elif result.role == "build":
            print(f"   🔧 Tools: {result.details.get('tools', '0')}")
            print(f"   🔨 Fixes: {result.details.get('fixes', '0')}")
            print(f"   🧪 Tests: {result.details.get('tests', '0')}")
            print(f"   📖 Documentation: {result.details.get('documentation', '0/0')}")

    def print_summary(self, results: List[EvaluationResult]):
        """Print summary of all evaluations.

        Args:
            results: List of EvaluationResult objects
        """
        print("\n" + "=" * 70)
        print("📊 Squad Evaluation Summary")
        print("=" * 70)

        # Sort by score
        sorted_results = sorted(results, key=lambda r: r.overall_score, reverse=True)

        for i, result in enumerate(sorted_results, 1):
            score_color = "🟢" if result.overall_score >= 75 else "🟡" if result.overall_score >= 50 else "🔴"
            print(f"\n{i}. {result.agent_name} — {score_color} {result.overall_score:.1f}/100 ({result.role.capitalize()})")

        print("\n" + "=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate squad agent performance with role-specific metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'agent',
        nargs='?',
        help='Agent to evaluate (marcus|galen|argus|archimedes)'
    )

    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Evaluate all agents'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    evaluator = SquadEvaluator()

    try:
        if args.all:
            results = evaluator.evaluate_all()
            evaluator.print_summary(results)

            if args.json:
                json_results = [
                    {
                        'agent_name': r.agent_name,
                        'role': r.role,
                        'score': r.overall_score,
                        'metrics': r.metrics,
                        'details': r.details,
                        'status': r.status,
                        'last_learning': r.last_learning,
                        'last_output': r.last_output
                    }
                    for r in results
                ]
                print("\n" + json.dumps(json_results, indent=2))

        elif args.agent:
            result = evaluator.evaluate(args.agent)
            evaluator.print_result(result)

            if args.json:
                json_result = {
                    'agent_name': result.agent_name,
                    'role': result.role,
                    'score': result.overall_score,
                    'metrics': result.metrics,
                    'details': result.details,
                    'status': result.status,
                    'last_learning': result.last_learning,
                    'last_output': result.last_output
                }
                print("\n" + json.dumps(json_result, indent=2))

        else:
            print("❌ Please specify an agent or use --all")
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Evaluation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import sys
    main()
