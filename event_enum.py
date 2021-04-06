from enum import Enum

Severity = Enum("Severity", "critical error warning info")
Action = Enum("Action", "trigger acknowledge resolve")
