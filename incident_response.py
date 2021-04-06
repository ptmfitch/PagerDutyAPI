from pdpyras import EventsAPISession, APISession
try:
    from api_auth import api_token, routing_key
except ImportError:
    print("Please add api_token and routing_key to api_auth.py")
    exit(1)
from time import sleep
from event_enum import Action, Severity
import json

event_session = EventsAPISession(routing_key)
api_session = APISession(api_token)

dms_address = "dms.ajubacorp.com"
preview_address = "preview.ajubacorp.com"
ai_address = "ai.ajubacorp.com"


# https://developer.pagerduty.com/docs/events-api-v2/trigger-events/
def trigger_event(summary, source, severity):
    payload = {
        "summary": summary,
        "source": dms_address,
        "severity": severity.name
    }
    print("Triggering event: \"{}\"".format(summary))
    return event_session.send_event(Action.trigger.name, payload=payload)


def acknowledge_event(dedup_key):
    print("Acknowledging issue {}".format(dedup_key))
    event_session.send_event(Action.acknowledge.name, dedup_key)
    print("Issue {} acknowledged".format(dedup_key))


def resolve_event(dedup_key):
    print("Resolving issue {}".format(dedup_key))
    event_session.send_event(Action.resolve.name, dedup_key)
    print("Issue {} resolved".format(dedup_key))


dk = trigger_event("User unable to save document", dms_address, Severity.error)

print("Attempting to resolve issue {} automatically".format(dk))
sleep(2)
acknowledge_event(dk)
sleep(0.5)
print("Waiting for decreased server load to resend save request")
sleep(2)
print("Resending save request")
sleep(0.5)
print("Save response code returned 200")
resolve_event(dk)
print("Issue resolved automatically")


# https://pagerduty.github.io/pdpyras/#events-api-client
def trigger_incident(summary, source, severity):
    print("Triggering incident: {}".format(summary))
    return event_session.trigger(summary, source, severity=severity.name)

# print(trigger_incident("User cannot preview document", preview_address, Severity.error))
# print(trigger_incident("No response received from classification after 30s", ai_address, Severity.warning))


# https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1incidents~1%7Bid%7D~1log_entries/get
def get_incident_log(incident_id):
    log_entries = api_session.get("incidents/{}/log_entries".format(incident_id))
    with open("incident_{}.json".format(incident_id), "w") as out_file:
        print("Writing incident log entries to {}".format(out_file.name))
        response_json = json.loads(log_entries.text)
        json_object = json.dumps(response_json, indent=4)
        out_file.write(json_object)
    print("Done")

# get_incident_log("P1JVQKY")
