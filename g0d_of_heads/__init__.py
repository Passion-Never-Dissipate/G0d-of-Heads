from mcdreforged.api.all import *


def on_load(server: PluginServerInterface, old):
    server.register_help_message('!!head <player> [个数]', '获取指定玩家的头颅,支持同时获取多个。当count未指定时，默认值为1。本插件支持全版本。')
    builder = SimpleCommandBuilder()
    builder.command("!!head <player>", give_heads)
    builder.command("!!head <player> <count>", give_heads)
    builder.arg("player", Text)
    builder.arg("count", lambda count: Integer(count).at_min(1))
    builder.register(server)


def give_heads(source: InfoCommandSource, dic: dict):
    if not source.is_player:
        source.reply("§c§l指令来源为非玩家，请重试")
        return

    owner = source.get_info().player
    player = dic["player"]
    version = Version(ServerInterface.get_instance().get_server_information().version)
    ver_mapping = {
        (Version("1.20.5+"),None): 2,
        (Version("1.13"), Version("1.20.5")): 1,
        (None, Version("1.13")): 0
    }
    val = next(
        (
            value for (min_ver, max_ver), value in ver_mapping.items()
                 if (min_ver is None or version >= min_ver) and (max_ver is None or version < max_ver)
        ),
        0
    )
    command_mapping = {
        2: f'/give {owner} minecraft:player_head[minecraft:profile="{player}"] {1 if "count" not in dic else dic["count"]}',
        1: f'/give {owner} minecraft:player_head{{SkullOwner:"{player}"}} {1 if "count" not in dic else dic["count"]}',
        0: f'/give {owner} minecraft:skull {1 if "count" not in dic else dic["count"]} 3 {{SkullOwner:"{player}"}}'
    }
    command = command_mapping.get(val, command_mapping[2])
    source.get_server().execute(command)
    source.reply(f"§bGOH: {owner} 获取了{1 if "count" not in dic else dic["count"]}个 {player} 的头颅")
