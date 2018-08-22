from vkApiAccess import *
import json, sys
import time, datetime


def collectFromList(list_of_lists):
    # in - [[1,2,3], [4,[5,6,7],[8],9]]
    # out - [1,2,3,4,5,6,7,8,9]
    result = []
    for i in list_of_lists:
        if type(i) == list:
            result += collectFromList(i)
        else:
            result.append(i)
    return result


def loadConfig(cf = 'config.json'):
    f = open(cf, 'r', encoding='utf8').read()
    c = json.loads(f)
    return c


def loadVkCode(f):
    code = open(f, encoding='utf8').read()
    return code


def loadMessages(peer_id, user_id, access_token):

    msgs_gl = []

    offset = 0
    msgs = callVkApi('messages.getHistory', access_token, count = 200, offset = 0, peer_id = peer_id, user_id = user_id, rev = 0)
    msgs_count = msgs['count']
    print('messages to collect: %s'%(msgs_count))

    strt = datetime.datetime.now()

    while offset < msgs_count + 200:

        code = loadVkCode('loadMessages.vkcode')
        code = code.format(offset, peer_id, user_id)
        code = code.replace('+', '%2B')

        returned = callVkApi('execute', access_token, code=code)
        offset_ = returned[0]
        new_msgs = returned[1] ## WARNING: this is a list of vk response objects
        
        _msgs = [i['items'] for i in new_msgs if i['items'] != []]
        _msgs = collectFromList(_msgs)
        
        msgs_gl += _msgs
        offset = offset_
        time.sleep(0.3333333)
        sys.stdout.write('\rcollected %s messages'%(len(msgs_gl)))
        sys.stdout.flush()

    fnsh = datetime.datetime.now()
    print('\nelapsed time: %s\n'%(fnsh-strt))

    return collectFromList(msgs_gl)


def tableOfMessages(fname, messages_list):

    f = open(fname, 'w', encoding='utf8')

    all_keys = {}
    for message_object in messages_list:
        ks = message_object.keys()
        for k in ks:
            all_keys[k] = 1

    head = all_keys.keys()
    print('\t'.join(head), file=f)

    for message_object in messages_list:
        table_row = []
        for message_item in head:
            try:
                row_item = repr(message_object[message_item])
            except Exception as e:
                row_item = ''
            table_row.append(row_item)
        table_row = '\t'.join(table_row)

        print(table_row, file=f)

    f.close()

    return None


def main():
    config = loadConfig()
    peer_ids = config['peer_id']
    user_id = config['user_id']
    access_token = config['access_token']
    
    for peer_id in peer_ids:
        print('loading dialogue with %s'%peer_id)
        a = loadMessages(peer_id, user_id, access_token)
        result_fname = '%s.csv'%peer_id
        tableOfMessages(result_fname, a)

    return None


if __name__ == '__main__':
    main()