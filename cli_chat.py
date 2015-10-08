import random
import redis
import re

# coding=utf-8

max_words = 30
redis_con_tpb = redis.Redis(host='localhost', port='6379', db=0)
redis_con_office = redis.Redis(host='localhost', port='6379', db=1)
redis_con_arrdev = redis.Redis(host='localhost', port='6379', db=2)

def remove_punc(line):
    line = line.replace('\r', ' ').replace('\n', ' ').replace('\t',' ').replace('"', ' ')
    return re.sub(r'\(.*?\)', '',  line)

def analyze_input(phrase, db):
    message_tuples = []
    phrase = remove_punc(phrase.decode('utf-8').strip())
    phrase += ' <stop>'
    words = phrase.split()
    length = len(words)
    messages = []
    for i, word in enumerate(words):
        if i < length - 2:
            if db == 0:
                redis_con_tpb.sadd('-'.join([words[i],words[i+1]]), words[i+2])
            elif db ==1:
                redis_con_office.sadd('-'.join([words[i],words[i+1]]), words[i+2])
            elif db == 2:
                redis_con_arrdev.sadd('-'.join([words[i],words[i+1]]), words[i+2])
            message_tuples.append((words[i],words[i+1], words[i+2]))

    for words in message_tuples:
        longest = ''
        for i in range(10):
            gen_message = generate_message([words[0], words[1]], db)
            if len(gen_message) > len(longest):
                longest = gen_message
        if longest:
            messages.append(longest)

    if len(messages):
        return random.choice(messages)


    

def generate_message(words, db):
    gen_words = []

    for i in range(max_words):
        gen_words.append(words[0])

        next_word = None
        if db ==0:
            next_word = redis_con_tpb.srandmember('-'.join(words))
        elif db ==1:
            next_word = redis_con_office.srandmember('-'.join(words))
        elif db == 2:
            next_word = redis_con_arrdev.srandmember('-'.join(words))
        if not next_word:
            break

        words = [words[1], next_word]

    return ' '.join(x.decode('utf-8') for x in gen_words)

def chat_client():
    while True:
        user_response = raw_input()

        print analyze_input(user_response)


if __name__ == "__main__":
    chat_client()    

