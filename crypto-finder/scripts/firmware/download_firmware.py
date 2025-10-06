# Hinglish: Yeh script internet se firmware images download karke 'data/01_raw' directory me save karti hai.

import typer
import requests
from pathlib import Path
from crypto_finder.common.logging import log
from crypto_finder.common.config import settings

# Kuch sample firmware URLs (aap is list ko bada kar sakte hain)
FIRMWARE_URLS = [
    "https://downloads.openwrt.org/releases/22.03.5/targets/ath79/generic/openwrt-22.03.5-ath79-generic-tplink_archer-c7-v5-squashfs-sysupgrade.bin",
    "https://firmware.dlink.com/dap/dap-1650/driver/DAP-1650_fw_reva_103b02_ALL_en_20150304.zip"
]

app = typer.Typer()

@app.command()
def download(
    output_dir: Path = typer.Option(
        settings.raw_data_dir, 
        "--output-dir", 
        "-o", 
        help="Directory jahan firmware save karna hai."
    )
):
    """Downloads a list of firmware images from the internet."""
    log.info(f"Firmware download shuru ho raha hai, save location: {output_dir}")
    output_dir.mkdir(exist_ok=True)

    for url in FIRMWARE_URLS:
        filename = output_dir / url.split("/")[-1]
        
        if filename.exists():
            log.info(f"'{filename.name}' pehle se exist karta hai. Skipping.")
            continue

        try:
            log.info(f"Downloading {url}...")
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()  # Agar HTTP error ho to exception raise karega

            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            log.success(f"Successfully downloaded and saved to {filename}")
        
        except requests.exceptions.RequestException as e:
            log.error(f"'{url}' ko download karne me error aaya: {e}")

if __name__ == "__main__":
    app()