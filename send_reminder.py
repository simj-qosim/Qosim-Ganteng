import os
import json
import sys
import urllib.request
import urllib.error

def send_to_seatalk(message, reminder_name):
    """Fungsi utama untuk mengirim teks dan @All ke SeaTalk"""
    webhook_url = os.environ.get("SEATALK_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError(
            "SEATALK_WEBHOOK_URL tidak ditemukan. "
            "Pastikan sudah diset di environment variable."
        )

    # Payload khusus SeaTalk untuk mengaktifkan fitur Mention All
    payload = {
        "tag": "text",
        "text": {
            "content": message,
            "at_all": True  # <-- Fitur ini otomatis akan men-tag seluruh anggota grup
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
            "User-Agent": f"CronJob-SeaTalk-{reminder_name}/1.0",
        },
    )

    print("=================================")
    print(f"🚀 Triggering: {reminder_name}")
    print("=================================")

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status = response.status
            response_body = response.read().decode("utf-8", errors="replace")
            print(f"HTTP Status Code : {status}")
            if 200 <= status < 300:
                print(f"✅ {reminder_name} berhasil dikirim dengan mention @All.")
            else:
                raise RuntimeError(f"Gagal. Status {status}: {response_body}")
    except Exception as error:
        print(f"❌ Error pada {reminder_name}: {repr(error)}")
        raise

# =====================================================================
# INDIVIDU FUNGSI REMINDER (Masing-masing berdiri sendiri 1x kirim)
# =====================================================================

def reminder_1():
    msg = "⏰ Jangan lupa absen mas ganteng mba cantik dan jangan lupa berdoa 🙏"
    send_to_seatalk(msg, "Reminder 1 (Absen Pagi)")

def reminder_2():
    msg = "📊 Report total accountnya disini ya ganteng cantik, tulis rata-ratanya dan kalian sudah dapat berapa, kalo under jangan lupa bilang ke TL atau TL Row 🙏"
    send_to_seatalk(msg, "Reminder 2 (Report TL)")

def reminder_3():
    msg = "Selamat pagi teman-teman sekedar mengingatkan untuk CBD nya semisal ketemu case hard complain,wpwn,suspect froud,dan ec do not itu diimput cbdnya h+4 23.59 untuk PTP H+3 teman-teman semangat.\njangan lupa di react ya"
    send_to_seatalk(msg, "Reminder 3 (CBD Pagi)")

def reminder_4():
    msg = "Report total accountnya lagi disini ya ganteng cantik,tulis rata-ratanya berapa dan kalian sudah dapat berapa, kalo under stop FU Callnya lagi"
    send_to_seatalk(msg, "Reminder 4 (Report Stop FU 1)")

def reminder_5():
    msg = "Jangan lupa FU Callnya, connect 1jt up 100% dan attamp all user 20X durasi ringing 5 detik. Hindari attamp di nomor yang tidak aktif dan sejenisnya, sayang sama effort temen-temen"
    send_to_seatalk(msg, "Reminder 5 (FU Call 1)")

def reminder_6():
    msg = "S7 jangan lupa absen pulang dan S14 jangan lupa absen dan berdoa"
    send_to_seatalk(msg, "Reminder 6 (Absen S7 & S14)")

def reminder_7():
    msg = "Report total accountnya disini ya ganteng cantik, tulis rata-ratanya berapa dan kalian sudah dapat berapa, kalo under jangan lupa bilang ke TL atau TL Row"
    send_to_seatalk(msg, "Reminder 7 (Report TL 2)")

def reminder_8():
    msg = "Selamat sore teman-teman sekedar mengingatkan untuk CBD nya semisal ketemu case hard complain,wpwn,suspect froud,dan ec do not itu diimput cbdnya h+4 23.59 untuk PTP H+3 teman-teman semangat.\njangan lupa di react ya"
    send_to_seatalk(msg, "Reminder 8 (CBD Sore)")

def reminder_9():
    msg = "Jangan lupa FU Callnya, connect 1jt up 100% dan attamp all user 20X durasi ringing 5 detik. Hindari attamp di nomor yang tidak aktif dan sejenisnya, sayang sama effort temen-temen"
    send_to_seatalk(msg, "Reminder 9 (FU Call 2)")

def reminder_10():
    msg = "Report total accountnya lagi disini ya ganteng cantik,tulis rata-ratanya berapa dan kalian sudah dapat berapa, kalo under stop FU Callnya lagi"
    send_to_seatalk(msg, "Reminder 10 (Report Stop FU 2)")

def reminder_11():
    msg = "Jangan lupa script 8.8"
    send_to_seatalk(msg, "Reminder 11 (Script 8.8)")

def reminder_12():
    msg = "jangan lupa absen pulang"
    send_to_seatalk(msg, "Reminder 12 (Absen Pulang)")


if __name__ == "__main__":
    # Memetakan kode teks argumen langsung ke fungsinya masing-masing
    functions_map = {
        "r1": reminder_1, "r2": reminder_2, "r3": reminder_3, "r4": reminder_4,
        "r5": reminder_5, "r6": reminder_6, "r7": reminder_7, "r8": reminder_8,
        "r9": reminder_9, "r10": reminder_10, "r11": reminder_11, "r12": reminder_12
    }
    
    # Default ke r1 jika tidak ada argumen masuk
    msg_type = "r1"
    
    # Mengamankan pembacaan input argument agar tidak error bertipe list
    if len(sys.argv) > 1:
        raw_input = sys.argv[1]
        msg_type = raw_input.strip().lower()
        
    if msg_type in functions_map:
        functions_map[msg_type]()
    else:
        print(f"❌ Kode reminder '{msg_type}' tidak ditemukan. Gunakan r1 sampai r12.")
