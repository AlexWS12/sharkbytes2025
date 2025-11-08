import os
import requests
from datetime import datetime

def send_discord_alert(event_type: str, description: str, severity: str, image_url: str = None):
    """Send an alert message to Discord using an embed."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ No Discord webhook URL found in .env")
        return

    severity_emojis = {
        "info": "🟢",
        "warning": "🟠",
        "critical": "🔴"
    }

    color_map = {
        "info": 0x00FF00,
        "warning": 0xFFA500,
        "critical": 0xFF0000
    }

    emoji = severity_emojis.get(severity, "⚪")
    color = color_map.get(severity, 0x808080)

    embed = {
        "title": f"{emoji} Security Alert - {severity.upper()}",
        "description": description,
        "color": color,
        "fields": [
            {"name": "Event Type", "value": event_type, "inline": True},
            {"name": "Severity", "value": severity, "inline": True}
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

    if image_url:
        embed["image"] = {"url": image_url}

    payload = {"embeds": [embed]}

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"✅ Sent Discord alert: {severity.upper()} - {description[:60]}")
    except Exception as e:
        print(f"❌ Failed to send Discord alert: {e}")
