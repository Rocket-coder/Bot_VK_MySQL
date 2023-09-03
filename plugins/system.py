import requests.exceptions
import vk_api
from plugins.tokens import token
import plugins.mysql as SQL
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

image = "photo-220949620_457239018"


#The file with the token has been removed for security reasons.


def session():
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session, wait=90)
    return [vk, longpoll, vk_session]

list = session()
vk = list[0]
longpoll = list[1]
vk_session = list[2]

def sender(user_id, text):
    vk_session.method('messages.send', {'user_id': user_id, 'message':text, 'random_id':get_random_id()})

def img_send(user_id, url):
    vk_session.method('messages.send', {'user_id': user_id, 'attachment': url, 'random_id': get_random_id()})

def get_user_name(user_id):
    user = vk_session.method('users.get', {'user_ids':user_id})
    return user[0]['first_name']
def start():
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    user_id = event.user_id
                    reg = SQL.new_or_old(user_id)
                    if reg == 0:
                        if (msg == 'биология') or (msg == 'химия'):
                            reg = 1
                            SQL.insert(user_id, get_user_name(user_id), msg)
                            prof_user_id = SQL.chim_or_bio(user_id)
                            hi = SQL.hi(prof_user_id)
                            sender(user_id, hi)
                            img_send(user_id, image)

                        else:
                            sender(user_id, f'{get_user_name(user_id)}, давай выберем науку (биология или химия)!')
                    #проверка текущего кода
                    else:
                        prof_user_id = SQL.chim_or_bio(user_id)
                        if prof_user_id == 3:
                            print(f'У пользователя {user_id} ошибка в профессии!')
                            sender(user_id, 'Упс, что-то пошло не так...')
                            continue


                        stat = SQL.get_status(user_id)
                        if stat is None:
                            stat = 1

                        if stat == 8:
                            sender(user_id, "Я же сказал, что я мухо... тьфу, устал и ухожу!")
                            continue

                        else:
                            stat = stat + 1

                        if prof_user_id == 1 and stat == 2:
                            c1 = SQL.get_code(stat, prof_user_id)
                            c2 = SQL.get_code(9, prof_user_id)

                            code = [c1, c2]

                            if msg in code:
                                SQL.change_status(user_id)
                                stat = SQL.get_status(user_id)
                                print(stat)
                                tmp = SQL.mess(stat, prof_user_id)
                                sender(user_id, tmp)
                                continue

                        if prof_user_id == 2 and stat == 6:
                            c1 = SQL.get_code(stat, prof_user_id)
                            c2 = SQL.get_code(9, prof_user_id)

                            code = [c1, c2]

                            if msg in code:
                                SQL.change_status(user_id)
                                stat = SQL.get_status(user_id)
                                print(stat)
                                tmp = SQL.mess(stat, prof_user_id)
                                sender(user_id, tmp)
                                continue

                        code = SQL.get_code(stat, prof_user_id)

                        if msg == code:
                            SQL.change_status(user_id)
                            stat = SQL.get_status(user_id)
                            print(stat)
                            tmp = SQL.mess(stat, prof_user_id)
                            sender(user_id, tmp)

                        else:
                            sender(user_id, 'Ой, что-то тут неправильно...')
        except requests.exceptions.ConnectionError:
            session()