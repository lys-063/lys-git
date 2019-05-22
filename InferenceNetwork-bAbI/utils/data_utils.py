import os
from utils.arguments import task_id, de
from utils.build_candidates import load_entity_dict, extract_entity, get_candidate_dict

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
f_dialogs_trn_name = 'dialogs-trn{}-{}.txt'.format(task_id, 'de' if de == True else 'le')
f_dialogs_tst_name = 'dialogs-tst{}-{}.txt'.format(task_id, 'de' if de == True else 'le')
f_data_trn_name = 'data-trn{}-{}.txt'.format(task_id, 'de' if de == True else 'le')
f_data_tst_name = 'data-tst{}-{}.txt'.format(task_id, 'de' if de == True else 'le')


def get_dialogs(src_file):
    dialogs = []
    dialog = []
    turn_cnt = 0
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
                    pass
            else:
                dialogs.append(dialog)
                dialog = []
                turn_cnt = 0
    return dialogs


def de_dialogs(raw_dialogs):
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


def next(src_file, n):
    dst_data = []
    for i in range(n):
        line = src_file.readline()
        if line:
            dst_data.append(eval(line))
        else:
            break
    return dst_data


def de_sentence(raw_sentence):
    s = raw_sentence.split()
    sentence = []
    for i in range(len(s)):
        word = s[i]
        entity = extract_entity(word)
        sentence.append(entity)
    sentence = ' '.join(sentence)
    return sentence


def get_dialog_max_length(dialogs):
    max_length = 0
    for dialog in dialogs:
        if len(dialog) > max_length:
            max_length = len(dialog)
    return max_length


def get_sentence_max_length(dialogs):
    max_length = 0
    for dialog in dialogs:
        for sentence in dialog:
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
        utterances.append(turn.split('\t')[0])
    return utterances


def get_responses(dialog):
    responses = []
    for turn in dialog:
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
    sentence_vectorized = []
    for word in sentence:
        if word in vocabulary.keys():
            sentence_vectorized.append(vocabulary[word])
        else:
            print('ERROR---' + str(word) + ' NOT FOUND')
    return sentence_vectorized


def vectorize_candidates(candidates, padding_size, vocabulary):
    candidates_vector = []
    for c in candidates:
        c = tokenize_padding(c, padding_size)
        candidates_vector.append([vocabulary[word] for word in c])
    return candidates_vector


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


print('IN data_utils')

print('GET candidate_dict')
candidate_dict = get_candidate_dict(de=de)

print('GET dialogs-trn')
try:
    f_dialogs_trn = open(utils_root + f_dialogs_trn_name, 'r')
except:
    f = open(utils_root + f_dialogs_trn_name, 'w')
    dialogs_trn = get_dialogs(data_root + f_raw_trn_name)
    if de == True:
        dialogs_trn = de_dialogs(dialogs_trn)
    for dialog in dialogs_trn:
        f.write(str(dialog) + '\n')
        f.flush()
    f.close()
    f_dialogs_trn = open(utils_root + f_dialogs_trn_name, 'r')

print('GET dialogs-tst')
try:
    f_dialogs_tst = open(utils_root + f_dialogs_tst_name, 'r')
except:
    f = open(utils_root + f_dialogs_tst_name, 'w')
    dialogs_tst = get_dialogs(data_root + f_raw_tst_name)
    if de == True:
        dialogs_tst = de_dialogs(dialogs_tst)
    for dialog in dialogs_tst:
        f.write(str(dialog) + '\n')
        f.flush()
    f.close()
    f_dialogs_tst = open(utils_root + f_dialogs_tst_name, 'r')
dialogs_trn = next(f_dialogs_trn, 2000)
dialogs_tst = next(f_dialogs_tst, 2000)
dialogs = dialogs_trn + dialogs_tst

print('GET vocabulary, memory_max_size, sentence_max_size, candidate_max_size, candidates_vector')
vocabulary = build_vocabulary(dialogs, candidate_dict)
memory_max_size = get_dialog_max_length(dialogs) * 2
sentence_max_size = get_sentence_max_length(dialogs)
candidate_max_size = get_candidate_max_length(candidate_dict)
candidates_vector = vectorize_candidates(candidate_dict.keys(), candidate_max_size, vocabulary)

print('GET data-trn')
try:
    f_data_trn = open(utils_root + f_data_trn_name, 'r')
except:
    f = open(utils_root + f_data_trn_name, 'w')
    for dialog in dialogs_trn:
        data_trn = get_data(dialog, memory_max_size, sentence_max_size, vocabulary, candidate_dict)
        for data_item in data_trn:
            f.write(str(data_item) + '\n')
        f.flush()
    f.close()
    f_data_trn = open(utils_root + f_data_trn_name, 'r')

print('GET data-tst')
try:
    f_data_tst = open(utils_root + f_data_tst_name, 'r')
except:
    f = open(utils_root + f_data_tst_name, 'w')
    for dialog in dialogs_tst:
        data_tst = get_data(dialog, memory_max_size, sentence_max_size, vocabulary, candidate_dict)
        for data_item in data_tst:
            f.write(str(data_item) + '\n')
        f.flush()
    f.close()
    f_data_tst = open(utils_root + f_data_tst_name, 'r')

print('OUT data_utils')
