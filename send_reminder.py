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

    message = "⏰ Jangan lupa absen mas ganteng mba cantik dan jangan lupa berdoa 🙏"

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
            "User-Agent": "GitHubActions-SeaTalk-Reminder/1.0",
        },
    )

    print("=================================")
    print("🚀 Sending message to SeaTalk...")
    print("=================================")

    try:
        # Timeout dibuat 10 detik supaya tidak menggantung lama
        with urllib.request.urlopen(request, timeout=10) as response:

            status = response.status
            response_body = response.read().decode("utf-8", errors="replace")

            print(f"HTTP Status Code : {status}")
            print(f"SeaTalk Response : {response_body}")

            if 200 <= status < 300:
                print("✅ Pesan berhasil dikirim ke SeaTalk.")
            else:
                raise RuntimeError(
                    f"SeaTalk mengembalikan HTTP status {status}: "
                    f"{response_body}"
                )

    except urllib.error.HTTPError as error:

        response_body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        print(f"❌ HTTP Error : {error.code}")
        print(f"❌ Response   : {response_body}")

        raise RuntimeError(
            f"SeaTalk HTTP Error {error.code}: {response_body}"
        ) from error

    except urllib.error.URLError as error:

        print(f"❌ URL Error : {error.reason}")

        raise RuntimeError(
            f"Gagal menghubungi SeaTalk: {error.reason}"
        ) from error

    except TimeoutError:

        print("❌ Request ke SeaTalk timeout.")

        raise RuntimeError(
            "SeaTalk tidak memberikan response dalam 10 detik."
        )

    except Exception as error:

        print(f"❌ Execution Error: {repr(error)}")
        raise


if __name__ == "__main__":
    send_seatalk_reminder()
