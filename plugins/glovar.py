# SCP-079-HIDE - Hide the real sender
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-HIDE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from configparser import RawConfigParser
from threading import Lock
from typing import Dict, List, Set, Union

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="log",
    filemode="a"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

# [custom]
aio: Union[bool, str] = ""
backup: Union[bool, str] = ""
hiders: Union[str, Set[str]] = ""
project_link: str = ""
project_name: str = ""
zh_cn: Union[bool, str] = ""

# [encrypt]
password: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")

    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))

    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", str(critical_channel_id)))
    debug_channel_id = int(config["channels"].get("debug_channel_id", str(debug_channel_id)))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", str(exchange_channel_id)))
    hide_channel_id = int(config["channels"].get("hide_channel_id", str(hide_channel_id)))
    test_group_id = int(config["channels"].get("test_group_id", str(test_group_id)))

    # [custom]
    aio = config["custom"].get("aio", aio)
    aio = eval(aio)
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    hiders = config["custom"].get("hiders", hiders)
    hiders = set(hiders.split())
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    zh_cn = config["custom"].get("zh_cn", zh_cn)

    zh_cn = eval(zh_cn)
    # [encrypt]
    password = config["encrypt"].get("password", password)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or critical_channel_id == 0
        or debug_channel_id == 0
        or exchange_channel_id == 0
        or hide_channel_id == 0
        or test_group_id == 0
        or aio not in {False, True}
        or backup not in {False, True}
        or hiders in {"", "[DATA EXPUNGED]"} or hiders == set()
        or project_link in {"", "[DATA EXPUNGED]"}
        or project_name in {"", "[DATA EXPUNGED]"}
        or zh_cn not in {False, True}
        or password in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Languages
lang: Dict[str, str] = {
    # Admin
    "admin": (zh_cn and "管理员") or "Admin",
    # Basic
    "colon": (zh_cn and "：") or ": ",
    "version": (zh_cn and "版本") or "Version",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Record
    "project": (zh_cn and "项目编号") or "Project"
}

# Init

all_commands: List[str] = ["version"]

locks: Dict[str, Lock] = {
    "receive": Lock()
}

sender: str = "HIDE"

should_hide: bool = False

version: str = "0.1.2"

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
