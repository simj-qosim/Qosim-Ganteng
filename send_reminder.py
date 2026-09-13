import os
import json
import urllib.request
import urllib.error


def send_seatalk_reminder():
    webhook_url = os.environ.get("SEATALK_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError(
            "SEATALK_WEBHOOK_URL tidak ditemukan. "
            "Pastikan sudah diset sebagai GitHub Actions Secret."
        )

    message = """⏰ Jangan lupa absen mas ganteng mba cantik dan jangan lupa berdoa
"""

    payload = {
        "tag": "text",
        "text": {
            "content": message
        }
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        webhook_url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    print("Sending message to SeaTalk...")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            response_body = response.read().decode("utf-8")

            print(f"HTTP Status Code: {status}")
            print(f"SeaTalk Response: {response_body}")

            if 200 <= status < 300:
                print("✅ Pesan berhasil dikirim ke SeaTalk.")
            else:
                raise RuntimeError(
                    f"SeaTalk mengembalikan HTTP status {status}: {response_body}"
                )

    except urllib.error.HTTPError as error:
        response_body = error.read().decode("utf-8", errors="replace")

        print(f"❌ HTTP Error: {error.code}")
        print(f"SeaTalk Response: {response_body}")

        raise

    except urllib.error.URLError as error:
        print(f"❌ URL Error: {error.reason}")
        raise

    except Exception as error:
        print(f"❌ Execution Error: {repr(error)}")
        raise


if __name__ == "__main__":
    send_seatalk_reminder()
