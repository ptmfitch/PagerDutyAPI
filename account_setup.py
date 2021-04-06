from pdpyras import APISession
try:
    from api_auth import api_token
except ImportError:
    print("Please add api_token to api_auth.py")
    exit(1)

# https://pagerduty.github.io/pdpyras/
session = APISession(api_token)


# https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1teams/post
def post_team(name, description):
    team_json = {
        "team": {
            "type": "team",
            "name": name,
            "description": description
        }
    }

    res = session.post("teams", json=team_json)
    print(res)


# post_team("CloudOps", "The Cloud Operations team for the DMS.")


# https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1escalation_policies/post
def post_escalation_policy(team_id, schedule_id):
    escalation_policy_json = {
        "escalation_policy": {
            "type": "escalation_policy",
            "name": "Engineering Escalation Policy",
            "escalation_rules": [
                {
                    "escalation_delay_in_minutes": 30,
                    "targets": [
                        {
                            "id": schedule_id,
                            "type": "schedule_reference"
                        }
                    ]
                }
            ],
            "services": [],
            "num_loops": 0,
            "teams": [
                {
                    "id": team_id,
                    "type": "team_reference"
                }
            ],
            "description": "This is the primary escalation policy for the Cloud Operations team.",
            "on_call_handoff_notifications": "if_has_services"
        }
    }

    res = session.post("escalation_policies", json=escalation_policy_json)
    print(res)

# post_escalation_policy("P8BP8W8", "PZ18RGD")


# https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1services/post
def post_service(escalation_policy_id):
    service_json = {
        "service": {
            "type": "service",
            "name": "Document Management System",
            "description": "Legal document management system cloud frontend.",
            "auto_resolve_timeout": 14400,
            "acknowledgement_timeout": 600,
            "status": "active",
            "escalation_policy": {
                "id": escalation_policy_id,
                "type": "escalation_policy_reference"
            },
            "incident_urgency_rule": {
                "type": "use_support_hours",
                "during_support_hours": {
                    "type": "constant",
                    "urgency": "high"
                },
                "outside_support_hours": {
                    "type": "constant",
                    "urgency": "low"
                }
            },
            "support_hours": {
                "type": "fixed_time_per_day",
                "time_zone": "America/Lima",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "days_of_week": [
                    1,
                    2,
                    3,
                    4,
                    5
                ]
            },
            "scheduled_actions": [
                {
                    "type": "urgency_change",
                    "at": {
                        "type": "named_time",
                        "name": "support_hours_start"
                    },
                    "to_urgency": "high"
                }
            ],
            "alert_creation": "create_alerts_and_incidents",
            "alert_grouping_parameters": {
                "type": "time",
                "config": {
                    "timeout": 2
                }
            }
        }
    }

    res = session.post("services", json=service_json)
    print(res)


# post_service("PLCJXHS")
