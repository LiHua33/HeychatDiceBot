import common.common
import conf.command as command
import conf.model as model
import user_module.dice as dice
import re

HelloWorldCommandID = "1848340234200219648"
RepeaterCommandID = "1848345518004043776"
DiceCommandID = "1848338810582007808"
BotID = 74508030

def on_use_bot_command(data):
    meta = {}
    if isinstance(data, dict):
        print('=====In Command====')
        print(data)
        print('============')
        meta = model.UseCommandData(**data)
        user_info = model.SenderInfo(**data['sender_info'])
    if meta and meta.command_info:
        command_id = meta.command_info.id
        if command_id == RepeaterCommandID:
            on_repeater(meta)
        elif command_id == HelloWorldCommandID:
            on_helloWorld(meta)
        elif command_id == DiceCommandID:
            on_dice(meta, user_info)

def on_repeater(meta):
    req = model.ChannelImSendReq(
        msg=meta.msg,
        msg_type=model.MSG_TYPE_MDTEXT,
        channel_id=meta.channel_base_info.channel_id,
        room_id=meta.room_base_info.room_id,
    )
    common.common.SendMessage(req)

def on_helloWorld(meta):
    """
    Print 'Hellow World' at request text channel
    """
    send_req = model.ChannelImSendReq(
        msg = 'Hello World',
        msg_type = model.MSG_TYPE_MDTEXT,
        channel_id = meta.channel_base_info.channel_id,
        room_id = meta.room_base_info.room_id,
    )
    common.common.SendMessage(send_req)

def on_dice(meta, user_info):
    """
    Dice tool
    """
    msg = meta.msg.strip()
    html_compa = ['&lt;', '&gt;', '&le;', '&ge;']
    raw_compa = ['<', '>', '<=', '>=']
    for i in range(len(html_compa)):
        msg = msg.replace(html_compa[i], raw_compa[i])

    ndN_find_patter = r"(?<=/roll)\s?\d+\s?d\s?\d+"
    ndN_str = re.findall(ndN_find_patter, msg)[0].strip()

    send_msg_list = []

    at_user_nick_str = str(user_info.room_nickname)
    if not at_user_nick_str:
        at_user_nick_str = str(user_info.nickname)
    at_user_str = '@{} \n\n'.format(at_user_nick_str) 
    send_msg_list.append(at_user_str)

    n = int(ndN_str.split('d')[0].strip())
    N = int(ndN_str.split('d')[1].strip())
    if n <= 0 or N <= 0:
        nN_error = True
        dice_result_str = 'Error: 输入参数非法'
        send_msg_list.append(dice_result_str)
    else:
        nN_error = False
        dice_result = dice.Ndn(n, N)
        dice_sum = sum(dice_result)
        dice_result_str = "骰子结果: {}; 骰子和为 {} \n\n".format(dice_result, dice_sum)
        send_msg_list.append(dice_result_str)

    k_find_patter = "(?<={}".format(ndN_str)  + r")\s?[+-]\s?\d+"
    k_str = re.findall(k_find_patter, msg)
    if (k_str) and not nN_error:
        addsub_k = k_str[0].strip()
        addsub_str = re.findall(r"[+-]", addsub_k)[0].strip()
        k = int(re.findall(r"\d+", addsub_k)[0])
        dice_sum = dice_sum
        if (addsub_str == '+'):
            dice_sum = dice_sum + k
        elif (addsub_str == '-'):
            dice_sum = dice_sum - k
        
        if (dice_sum < 0):
            dice_sum = 0
        sum_str = '叠加修正值 {} 后为 {}; \n\n'.format(addsub_k, dice_sum)
        send_msg_list.append(sum_str)
        
    compare_find_patter = r"[><=]{1,2}\s?\d+"
    compare_str = re.findall(compare_find_patter, msg)
    if (compare_str) and not nN_error:
        compare_sign = re.findall('[><=]+', compare_str[0])[0]
        compare_value = re.findall('\d+', compare_str[0])[0]
        compa_int = int(compare_value)

        equal_bool = dice_sum == compa_int
        greater_bool = dice_sum > compa_int
        less_bool = dice_sum < compa_int
        if compare_sign == '=' or compare_sign == '==':
            result_bool = equal_bool
        elif compare_sign == '>':
            result_bool = greater_bool
        elif compare_sign == '<':
            result_bool = less_bool
        elif compare_sign == '>=':
            result_bool = greater_bool | equal_bool
        elif compare_sign == '<=':
            result_bool = less_bool | equal_bool
        
        bool_str_dict = {True: '成功', False: '失败'}
        compa_str = '骰子结果与 {} 进行比较的结果是 {}'.format(compa_int, bool_str_dict[result_bool])
        send_msg_list.append(compa_str)

    send_msg_str = ''.join(send_msg_list)

    print(send_msg_str)
    
    send_req = model.ChannelImSendReq(
        msg = send_msg_str,
        msg_type = model.MSG_TYPE_MDTEXT,
        channel_id = meta.channel_base_info.channel_id,
        room_id = meta.room_base_info.room_id,
    )
    common.common.SendMessage(send_req)

class EventHandler:
    async def on_message(self, data):
        message_type = data["type"]
        message_data = data["data"]
        print('=====Event====')
        print(data)
        print('============')
        if message_type == model.MSG_TYPE_USECOMMAND:
            on_use_bot_command(message_data)


########## TEST CODE ############
if __name__ == "__main__":
    test_data = "Message_data: {'bot_id': 74508030, 'channel_base_info': {'channel_id': '3603936004755005442', 'channel_name': '文字频道', 'channel_type': 1}, 'command_info': {'id': '1848345518004043776', 'name': '/repeat', 'type': 0}, 'msg': '/repeat 复读命令:123', 'msg_id': '1848359178268917760', 'room_base_info': {'room_avatar': 'https://imgheybox.max-c.com/web/bbs/2024/06/15/fa5c0608297d4ea4b891d2ca0dbf0b2e.png', 'room_id': '3603936004716036096', 'room_name': '凌霄飞人'}, 'send_time': 1729518143619, 'sender_info': {'avatar': 'https://cdn.max-c.com/heybox/avatar/99177a436725ba171577dc0d43c46385', 'avatar_decoration': {'src_type': '', 'src_url': ''}, 'bot': False, 'level': 3, 'medals': None, 'nickname': 'LiHua33', 'roles': None, 'room_nickname': '', 'tag': None, 'user_id': 21558197\}\}"
    on_use_bot_command(test_data)