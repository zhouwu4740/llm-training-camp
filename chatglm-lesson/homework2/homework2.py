import os
import api
import data_types
import json
import random


zhang_ning = "张宁作为A公司信贷业务部的产品经理，专注于信贷产品的设计和管理。他凭借出色的专业知识和创新思维，成功领导团队开发了多款高效、用户友好的信贷产品，大幅提升了公司在市场上的竞争力"

li_xian = "李现担任A公司信贷业务部的应用架构师，专精于信贷系统的架构设计、管理与研发。他以其深厚的技术功底和前瞻性视角，不仅优化了现有系统架构，还引领团队创新研发，有效提高了系统性能和用户体验，是公司技术骨干。"


# 人物特征
character_zhangning = ''.join(list(api.generate_role_appearance(zhang_ning)))
character_lixian = ''.join(list(api.generate_role_appearance(li_xian)))

# 人物信息
characters = {
    'zhangning': {
        'name': '张宁',
        'character': character_zhangning,
    },
    'lixian': {
        'name': '李现',
        'character': character_lixian
    }
}
# 一方扮演 user，另一方扮演 bot
players = ['zhangning', 'lixian']
player_zhangning = players[0]
player_lixian = players[1]

# 获取CharacterMeta


def get_character_meta(user_player, bot_player):
    return api.CharacterMeta(
        user_name=characters[user_player]['name'],
        user_info=characters[user_player]['character'],
        bot_name=characters[bot_player]['name'],
        bot_info=characters[bot_player]['character'],
    )


def generate_dialogue(user, bot, history) -> str:
    """生成对话"""
    response = api.get_characterglm_response(
        history, get_character_meta(user, bot))
    return ''.join(list(response))


def generate_dialogues(init_msg: data_types.TextMsg, num_dialogues: int = 10):
    message_history = []
    message_history.append(init_msg)

    for i in range(0, num_dialogues):
        user_index = i % 2
        user = players[user_index]
        bot = players[1-user_index]
        content = generate_dialogue(user, bot, message_history)
        if not (content.startswith('（张宁说）') or content.startswith('（李现说）')):
            content = f"（{characters[bot]['name']}说）{content}"
        message_history.append(data_types.TextMsg(
            role=characters[bot]['name'], content=content))

    return message_history


if __name__ == '__main__':
    init_msg = data_types.TextMsg(
        role='张宁', content='（张宁说）信贷二期项目将启动，李现我们一起来梳理一下项目重要流程')
    message_history = generate_dialogues(init_msg=init_msg, num_dialogues=10)
    # 保存对话数据
    postfix = random.randint(0, 100)
    file_name = f'dialog_{postfix}.json'
    with open(f'dialog_{postfix}.json', 'w') as f:
        json.dump(message_history, f)
    print(f'对话数据已保存在 {os.path.join(os.curdir, file_name)} 文件中.')
