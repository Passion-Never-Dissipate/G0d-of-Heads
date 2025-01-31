import re
from mcdreforged.api.all import *

version = '1.0.0'

def on_load(server, params):
    server.logger.info('正在注册指令')
    server.register_help_message('!!head <玩家名称X> [获取个数Y]', '获取指定玩家X的头颅,获取Y个，当Y未指定时，默认值为1。')



def on_info(server: ServerInterface, info: Info):
    if info.is_player and info.content.find('!!head ') > -1:
        give_heads(server, info)



def give_heads(server, info):
    info.cancel_send_to_server()

    #正则解参,匹配格式
    match = re.match(r'^!!head\s+(\S+)(?:\s+(\d+))?$', info.content)
    if not match:
        server.reply(info, '指令格式错误！正确的格式为 !!head <player> [数量]。')
        return
    
    owner = info.player
    player = match.group(1)
    quantity = match.group(2) if match.group(2) is not None else 1
    message = '§b[GOH] 已给予你§f[{0}]§b个{1} 的头颅'.format(quantity,player)
    server.logger.info('GOH:{} 获取了 {} 的头颅'.format(owner, player))
    server.execute('execute at {0} run give {0} minecraft:player_head{{SkullOwner:"{1}"}} {2}'.format(owner, player, quantity))
    server.reply(info, message)