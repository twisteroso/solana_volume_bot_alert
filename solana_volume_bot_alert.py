import requests, time

def volume_spike_monitor():
    print("Solana volume spike detector (top 50 tokens)")
    last_vol = {}
    while True:
        r = requests.get("https://api.dexscreener.com/latest/dex/tokens?chain=solana&limit=50")
        for t in r.json().get("pairs", []):
            addr = t["pairAddress"]
            vol = float(t["volume"]["h24"])
            prev = last_vol.get(addr, 0)
            if prev and vol > prev * 3:  # 3x spike in 24h volume
                print(f"VOLUME SPIKE x{vol/prev:.1f}!\n"
                      f"{t['baseToken']['symbol']}\n"
                      f"Volume 24h: ${vol:,.0f}\n"
                      f"Price: ${float(t['priceUsd']):.10f}\n"
                      f"https://dexscreener.com/solana/{t['baseToken']['address']}\n"
                      f"{'-'*50}")
            last_vol[addr] = vol
        time.sleep(25)

if __name__ == "__main__":
    volume_spike_monitor()
