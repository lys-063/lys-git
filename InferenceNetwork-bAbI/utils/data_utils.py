from utils.arguments import task_id, DL
from utils.build_candidates import load_entity_dict, extract_entity, get_candidate_dict

import os

path = os.getcwd()
current_directory = path.split('/')[-1]
if current_directory == 'InferenceNetwork-bAbI':
    data_root = 'raw_data/'
    db_root = 'db/'
    utils_root = 'utils/'
else:
    data_root = '../raw_data/'
    db_root = '../db/'
    utils_root = '../utils/'

f_raw_trn_name = 'babi-task{}-trn.txt'.format(task_id)
f_raw_tst_name = 'babi-task{}-tst.txt'.format(task_id)
f_dialogs_trn_name = 'dialogs-trn{}-{}.txt'.format(task_id, 'DL' if DL == True else 'L')
f_dialogs_tst_name = 'dialogs-tst{}-{}.txt'.format(task_id, 'DL' if DL == True else 'L')
f_data_trn_name = 'data-trn{}-{}.txt'.format(task_id, 'DL' if DL == True else 'L')
f_data_tst_name = 'data-tst{}-{}.txt'.format(task_id, 'DL' if DL == True else 'L')


def get_raw_dialogs(src_file):
    dialogs = []
    dialog = []
    turn_cnt = 0
    highest_rate = 0
    with open(src_file) as src:
        lines = src.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                if '\t' in line:
                    u, r = line.split('\t')
                    u = u.split()[1:]
                    u.append('$u')
                    u.append('#{}'.format(turn_cnt))
                    u = ' '.join(u)
                    r = r.split()
                    r.append('$s')
                    r.append('#{}'.format(turn_cnt))
                    r = ' '.join(r)
                    line = u + '\t' + r
                    dialog.append(line)
                    turn_cnt = turn_cnt + 1
                else:
                    line = line.split(' ')[1:]
                    resto_name = line[0]
                    if highest_rate <= int(resto_name.split('_')[-1][0]):
                        dialog.append(line)
                        highest_rate = int(resto_name.split('_')[-1][0])
            else:
                dialog_tmp = dialog.copy()
                dialog = []
                for line in dialog_tmp:
                    if '\t' in line:
                        dialog.append(line)
                    else:
                        resto_name = line[0]
                        if int(resto_name.split('_')[-1][0]) >= highest_rate:
                            dialog.append(line)
                dialogs.append(dialog)
                dialog = []
                turn_cnt = 0
                highest_rate = 0
    return dialogs


def dl_sentence(raw_sentence):
    s = raw_sentence.split()
    sentence = []
    for i in range(len(s)):
        word = s[i]
        entity = extract_entity(word)
        sentence.append(entity)
    sentence = ' '.join(sentence)
    return sentence


def get_dialog_length(dialog):
    length = 0
    for line in dialog:
        if '\t' in line:
            length = length + 1
    return length


def get_dialog_max_length(dialogs):
    max_length = 0
    for dialog in dialogs:
        n_dialog = get_dialog_length(dialog)
        if n_dialog > max_length:
            max_length = n_dialog
    return max_length


def get_sentence_max_length(dialogs):
    max_length = 0
    for dialog in dialogs:
        for sentence in dialog:
            if '\t' in sentence:
                u, r = sentence.split('\t')
                u = u.split()
                r = r.split()
                if (len(u) > max_length):
                    max_length = len(u)
                if (len(r) > max_length):
                    max_length = len(r)
    return max_length


def get_candidate_max_length(candidate_dict):
    max_length = 0
    candidates = candidate_dict.keys()
    for c in candidates:
        n_c = len(c.split())
        if n_c > max_length:
            max_length = n_c
    return max_length


def build_vocabulary(dialogs, candidate_dict):
    vocabulary = dict()
    vocabulary['$'] = 0
    for dialog in dialogs:
        for sentence in dialog:
            if '\t' in sentence:
                u, r = sentence.split('\t')
                u_words = u.split()
                r_words = r.split()
                for word in u_words:
                    if word not in vocabulary.keys():
                        vocabulary[word] = len(vocabulary.keys())
                for word in r_words:
                    if word not in vocabulary.keys():
                        vocabulary[word] = len(vocabulary.keys())
    candidates = candidate_dict.keys()
    for candidate in candidates:
        for word in candidate.split():
            if word not in vocabulary.keys():
                vocabulary[word] = len(vocabulary.keys())
    return vocabulary


def get_utterances(dialog):
    utterances = []
    for turn in dialog:
        if '\t' in turn:
            utterances.append(turn.split('\t')[0])
    return utterances


def get_responses(dialog):
    responses = []
    for turn in dialog:
        if '\t' in turn:
            responses.append(turn.split('\t')[1])
    return responses


def get_responses_id(responses, candidate_dict):
    responses_id = []
    for r in responses:
        r = r.strip().split()
        r = r[:-2]
        r = ' '.join(r)
        if r in candidate_dict.keys():
            responses_id.append(candidate_dict[r])
        else:
            responses_id.append(-1)
            print('ERROR---' + r)
    return responses_id


def tokenize_padding(sentence, padding_size):
    sentence = sentence.split()
    for i in range(padding_size - len(sentence)):
        sentence.append('$')
    return sentence


def vectorize_sentence(sentence, vocabulary):
    sentence_vector = []
    for word in sentence:
        if word in vocabulary.keys():
            sentence_vector.append(vocabulary[word])
        else:
            print('ERROR---' + str(word) + ' NOT FOUND')
    return sentence_vector


def vectorize_candidates(candidates, padding_size, vocabulary):
    candidates_vector = []
    for c in candidates:
        c = tokenize_padding(c, padding_size)
        candidates_vector.append([vocabulary[word] for word in c])
    return candidates_vector


def get_dialog_fmt(dialog, memory_size, padding_size, candidate_dict):
    n_turn = get_dialog_length(dialog)
    turn_cnt = 0
    n_dialog = len(dialog)
    dialog_fmt = []
    context = []
    entities = {'<name>': ['<name>'], '<cuisine>': ['<cuisine>'], '<location>': ['<location>'],
                '<number>': ['<number>'], '<price>': ['<price>'], '<address>': ['<address>'],
                '<phone>': ['<phone>'], '<api>': ['<api>']}
    utterances = get_utterances(dialog)
    responses = get_responses(dialog)
    responses_dl = []
    for i in range(len(responses)):
        responses_dl.append(dl_sentence(responses[i]))
    responses_id = get_responses_id(responses_dl, candidate_dict)

    for i in range(n_dialog):
        line = dialog[i]
        if '\t' in line:
            entities_tmp = {}
            for key in entities.keys():
                entities_tmp[key] = entities[key].copy()
            u = utterances[turn_cnt]
            r = responses[turn_cnt]
            u_token = tokenize_padding(u, padding_size)
            r_token = tokenize_padding(r, padding_size)
            for j in range(padding_size):
                u_word = u_token[j]
                u_entity = extract_entity(u_word)
                if u_entity != u_word:
                    entities[u_entity].append(u_word)
                u_token[j] = u_entity

                r_word = r_token[j]
                r_entity = extract_entity(r_word)
                if r_entity != r_word:
                    entities[r_entity].append(r_word)
                r_token[j] = r_entity

            response = responses[turn_cnt].split(' ')[:-2]
            response = ' '.join(response)
            context_tmp = context.copy() + [['$'] * padding_size] * (memory_size - len(context))
            dialog_fmt.append([context_tmp, entities_tmp, u_token, responses_id[turn_cnt], response])
            context.append(u_token)
            context.append(r_token)
            turn_cnt = turn_cnt + 1
        else:
            if line[0] not in entities['<name>']:
                entities['<name>'].append(line[0])
            if 'rating' not in line[1]:
                entities['<{}>'.format(line[1].split('_')[1])].append(line[2])
    return dialog_fmt


    for i in range(n_dialog):
        entities_tmp = {}
        for key in entities.keys():
            entities_tmp[key] = entities[key].copy()
        u = utterances[i]
        r = responses[i]
        u_token = tokenize_padding(u, padding_size)
        r_token = tokenize_padding(r, padding_size)
        for j in range(padding_size):
            u_word = u_token[j]
            u_entity = extract_entity(u_word)
            if u_entity != u_word:
                entities[u_entity].append(u_word)
            u_token[j] = u_entity

            r_word = r_token[j]
            r_entity = extract_entity(r_word)
            if r_entity != r_word:
                entities[r_entity].append(r_word)
            r_token[j] = r_entity

        response = responses[i].split(' ')[:-2]
        response = ' '.join(response)
        context_tmp = context.copy() + [['$'] * padding_size] * (memory_size - len(context))
        dialog_fmt.append([context_tmp, entities_tmp, u_token, responses_id[i], response])
        context.append(u_token)
        context.append(r_token)
    return dialog_fmt


def get_data_fmt(dialog_fmt, vocabulary):
    data_fmt = []
    for dialog_turn in dialog_fmt:
        context = dialog_turn[0]
        n_context = len(context)
        u_token = dialog_turn[2]
        context_vector = []
        u_token_vector = []
        for i in range(n_context):
            context_vector.append(vectorize_sentence(context[i], vocabulary))
        u_token_vector = vectorize_sentence(u_token, vocabulary)
        data_fmt.append([context_vector, dialog_turn[1], u_token_vector, dialog_turn[3], dialog_turn[4]])
    return data_fmt


def next(src_file, n):
    dst_data = []
    for i in range(n):
        line = src_file.readline()
        if line:
            dst_data.append(eval(line))
        else:
            break
    return dst_data


print('IN data_utils')

print('GET candidate_dict')
candidate_dict = get_candidate_dict(DL=DL)

print('GET raw_dialogs')
raw_dialogs_trn = get_raw_dialogs(data_root + f_raw_trn_name)
raw_dialogs_tst = get_raw_dialogs(data_root + f_raw_tst_name)
raw_dialogs = raw_dialogs_trn + raw_dialogs_tst

'''
with open('raw_dialogs_trn{}.txt'.format(task_id), 'w') as f:
    for raw_dialog_trn in raw_dialogs_trn:
        f.write(str(raw_dialog_trn) + '\n')
with open('raw_dialogs_tst{}.txt'.format(task_id), 'w') as f:
    for raw_dialog_tst in raw_dialogs_tst:
        f.write(str(raw_dialog_tst) + '\n')
'''

print('GET vocabulary, memory_max_size, sentence_max_size, candidate_max_size, candidates_vector')
vocabulary = build_vocabulary(raw_dialogs, candidate_dict)
memory_max_length = get_dialog_max_length(raw_dialogs) * 2
sentence_max_length = get_sentence_max_length(raw_dialogs)
candidate_max_length = get_candidate_max_length(candidate_dict)
candidates_vector = vectorize_candidates(candidate_dict.keys(), candidate_max_length, vocabulary)

print('GET dialogs_trn')
try:
    f_dialogs_trn = open(utils_root + f_dialogs_trn_name, 'r')
except:
    f = open(utils_root + f_dialogs_trn_name, 'w')
    for dialog in raw_dialogs_trn:
        dialog_trn = get_dialog_fmt(dialog, memory_max_length, sentence_max_length, candidate_dict)
        f.write(str(dialog_trn) + '\n')
        f.flush()
    f.close()
    f_dialogs_trn = open(utils_root + f_dialogs_trn_name, 'r')

print('GET dialogs_tst')
try:
    f_dialogs_tst = open(utils_root + f_dialogs_tst_name, 'r')
except:
    f = open(utils_root + f_dialogs_tst_name, 'w')
    for dialog in raw_dialogs_tst:
        dialog_tst = get_dialog_fmt(dialog, memory_max_length, sentence_max_length, candidate_dict)
        f.write(str(dialog_tst) + '\n')
        f.flush()
    f.close()
    f_dialogs_tst = open(utils_root + f_dialogs_tst_name, 'r')
dialogs_trn = next(f_dialogs_trn, 2000)
dialogs_tst = next(f_dialogs_tst, 2000)

print('GET data_trn')
try:
    f_data_trn = open(utils_root + f_data_trn_name, 'r')
except:
    f = open(utils_root + f_data_trn_name, 'w')
    for dialog_trn in dialogs_trn:
        data_trn = get_data_fmt(dialog_trn, vocabulary)
        for data_item in data_trn:
            f.write(str(data_item) + '\n')
        f.flush()
    f.close()
    f_data_trn = open(utils_root + f_data_trn_name, 'r')

print('GET data_tst')
try:
    f_data_tst = open(utils_root + f_data_tst_name, 'r')
except:
    f = open(utils_root + f_data_tst_name, 'w')
    for dialog_tst in dialogs_tst:
        data_tst = get_data_fmt(dialog_tst, vocabulary)
        for data_item in data_tst:
            f.write(str(data_item) + '\n')
        f.flush()
    f.close()
    f_data_tst = open(utils_root + f_data_tst_name, 'r')

print('OUT data_utils')

def get_accuracy(predictions, data, candidate_dict):
    n_correct = 0
    n_data = len(data)
    candidates = []
    for key in candidate_dict.keys():
        candidates.append(key)
    for i in range(n_data):
        entities = data[i][1]
        p = predictions[i]
        candidate = candidates[p]
        words = candidate.split(' ')
        n_words = len(words)
        for j in range(n_words):
            word = words[j]
            if word == '<name>':
                words[j] = entities['<name>'][-1]
            elif word == '<cuisine>':
                words[j] = entities['<cuisine>'][-1]
            elif word == '<location>':
                words[j] = entities['<location>'][-1]
            elif word == '<number>':
                words[j] = entities['<number>'][-1]
            elif word == '<price>':
                words[j] = entities['<price>'][-1]
            elif word == '<address>':
                words[j] = entities['<address>'][-1]
            elif word == '<phone>':
                words[j] = entities['<phone>'][-1]
            elif word == '<api>':
                words[j] = 'api_call'
            else:
                pass
        predict = ' '.join(words)
        if predict == data[i][4]:
            n_correct = n_correct + 1
        else:
            '''
            print('------------------')
            print('entities =' + '\n' + str(entities))
            print('predict = ' + predict)
            print('response = ' + data[i][4])
            print('------------------')
            '''
            pass
    return n_correct / n_data


'''
def dl_dialogs(raw_dialogs):
    dialogs = []
    for raw_dialog in raw_dialogs:
        dialog = []
        for sentence in raw_dialog:
            u, r = sentence.split('\t')
            u = u.split()
            r = r.split()
            utterance = []
            response = []
            for i in range(len(u)):
                word = u[i]
                entity = extract_entity(word)
                utterance.append(entity)
            utterance = ' '.join(utterance)
            for i in range(len(r)):
                word = r[i]
                entity = extract_entity(word)
                response.append(entity)
            response = ' '.join(response)
            dialog.append(utterance + '\t' + response)
        dialogs.append(dialog)
    return dialogs

def get_data(dialog, memory_size, padding_size, vocabulary, candidate_dict):
    data = []  # (context, utterance, response, response_id)
    context = []
    utterances_vector = []  # []
    responses_vector = []  # []
    utterances = get_utterances(dialog)
    responses = get_responses(dialog)
    responses_id = get_responses_id(responses, candidate_dict)

    for u in utterances:
        u_token = tokenize_padding(u, padding_size)
        u_vector = vectorize_sentence(u_token, vocabulary)
        utterances_vector.append(u_vector)

    for r in responses:
        r_token = tokenize_padding(r, padding_size)
        r_vector = vectorize_sentence(r_token, vocabulary)
        responses_vector.append(r_vector)

    for i in range(len(dialog)):
        context_tmp = context.copy() + [[0] * padding_size] * (memory_size - len(context))
        data.append((context_tmp, utterances_vector[i], responses_id[i]))
        context.append(utterances_vector[i])
        context.append(responses_vector[i])

    return data
'''
