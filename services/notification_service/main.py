from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from libs.events import publish_event
from libs.tenant_sdk import get_tenant_metadata

app = FastAPI(title="Notification Service", version="0.1.0")


class NotificationRequest(BaseModel):
    channel: str
    recipient: str
    message: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "notification_service"}


@app.post("/notifications/send")
async def send_notification(
    payload: NotificationRequest, x_tenant_id: str = Header(alias="X-Tenant-ID")
) -> dict[str, str]:
    try:
        tenant = get_tenant_metadata(x_tenant_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    event_payload = {
        "tenant_id": tenant.tenant_id,
        "channel": payload.channel,
        "recipient": payload.recipient,
        "message": payload.message,
    }
    await publish_event("notification.sent", event_payload)

    return {
        "tenant_id": tenant.tenant_id,
        "channel": payload.channel,
        "recipient": payload.recipient,
        "status": "queued",
    }
