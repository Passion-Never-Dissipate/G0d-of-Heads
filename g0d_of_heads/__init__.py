from mcdreforged.api.all import *


def on_load(server: PluginServerInterface, old):
    server.register_help_message('!!head <player> [个数]', '获取指定玩家的头颅,支持同时获取多个。')
    builder = SimpleCommandBuilder()
    builder.command("!!head <player>", give_heads)
    builder.command("!!head <player> <count>", give_heads)
    builder.arg("player", Text)
    builder.arg("count", lambda count: Integer(count).at_min(1))
    builder.register(server)


def give_heads(source: InfoCommandSource, dic: dict):
    if not source.is_player:
        source.reply("§c§l只有玩家才能使用该插件！！")
        return

    owner = source.get_info().player
    player = dic["player"]
    version = ServerInterface.get_instance().get_server_information().version
    val = 0 if version and Version(version) < Version("1.21") else 1
    insert = f'[minecraft:profile="{player}"]' if val else f'{{SkullOwner:"{player}"}}'
    source.get_server().execute(
        f'execute at {owner} run give {owner} minecraft:player_head{insert} {1 if "count" not in dic else dic["count"]}'
    )
    source.reply(f"§bGOH: {owner} 获取了 {player} 的头颅")
