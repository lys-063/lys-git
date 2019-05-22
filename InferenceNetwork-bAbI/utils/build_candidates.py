import os
from utils.arguments import task_id, de

path = os.getcwd()
current_directory = path.split('/')[-1]
if current_directory == 'InferenceNetwork-bAbI':
    data_root = 'raw_data/'
    db_root = 'db/'
else:
    data_root = '../raw_data/'
    db_root = '../db/'
f_raw_candidates_name = 'babi-candidates.txt'
f_raw_trn_name = 'babi-task{}-trn.txt'.format(task_id)
f_raw_tst_name = 'babi-task{}-tst.txt'.format(task_id)
f_candidate_dict_name = 'candidate_dict_{}.txt'.format('de' if de == True else 'le')
names = []
cuisines = []
locations = []
numbers = []
prices = []
addresses = []
post_codes = []
phones = []
api_call = ['api_call']


def build_entity_dict(src_root=data_root):
    # build entity_dict from babi-candidates.txt, trn.txt, tst.txt
    src_file = src_root + f_raw_candidates_name
    with open(src_file) as src:
        lines = src.readlines()
        for line in lines:
            words = line.strip().split(' ')
            if words[1] == 'api_call':
                if words[2] not in cuisines:
                    cuisines.append(words[2])
                if words[3] not in locations:
                    locations.append(words[3])
                if words[4] not in numbers:
                    numbers.append(words[4])
                if words[5] not in prices:
                    prices.append(words[5])
            else:
                for word in words[1:]:
                    if '_' in word:
                        if 'address' in word and word not in addresses:
                            addresses.append(word)
                        elif 'phone' in word and word not in phones:
                            phones.append(word)
                        else:
                            if word not in names:
                                names.append(word)
                    else:
                        pass
    src_file = src_root + f_raw_trn_name
    with open(src_file) as src:
        lines = src.readlines()
        for line in lines:
            if line:
                line = line.strip().split(' ', 1)[1]
                if '\t' in line:
                    u, r = line.split('\t')
                    if 'api_call' in r:
                        words = r.split(' ')
                        if words[1] not in cuisines:
                            cuisines.append(words[1])
                        if words[2] not in locations:
                            locations.append(words[2])
                        if words[3] not in numbers:
                            numbers.append(words[3])
                        if words[4] not in prices:
                            prices.append(words[4])
                else:
                    words = line.split(' ')
                    if words[0] not in names:
                        names.append(words[0])
                    if words[1] == 'R_cuisine':
                        cuisines.append(words[2])
                    elif words[1] == 'R_location':
                        locations.append(words[2])
                    elif words[1] == 'R_number':
                        numbers.append(words[2])
                    elif words[1] == 'R_price':
                        prices.append(words[2])
                    elif words[1] == 'R_address':
                        addresses.append(words[2])
                    elif words[1] == 'R_post_code':
                        post_codes.append(words[2])
                    elif words[1] == 'R_phone':
                        phones.append(words[2])
                    else:
                        print('ERROR---' + words[1])
            else:
                continue
    src_file = src_root + f_raw_tst_name
    with open(src_file) as src:
        lines = src.readlines()
        for line in lines:
            if line:
                line = line.strip().split(' ', 1)[1]
                if '\t' in line:
                    u, r = line.split('\t')
                    if 'api_call' in r:
                        words = r.split(' ')
                        if words[1] not in cuisines:
                            cuisines.append(words[1])
                        if words[2] not in locations:
                            locations.append(words[2])
                        if words[3] not in numbers:
                            numbers.append(words[3])
                        if words[4] not in prices:
                            prices.append(words[4])
                else:
                    words = line.split(' ')
                    if words[0] not in names:
                        names.append(words[0])
                    if words[1] == 'R_cuisine':
                        cuisines.append(words[2])
                    elif words[1] == 'R_location':
                        locations.append(words[2])
                    elif words[1] == 'R_number':
                        numbers.append(words[2])
                    elif words[1] == 'R_price':
                        prices.append(words[2])
                    elif words[1] == 'R_address':
                        addresses.append(words[2])
                    elif words[1] == 'R_post_code':
                        post_codes.append(words[2])
                    elif words[1] == 'R_phone':
                        phones.append(words[2])
                    else:
                        print('ERROR---' + words[1])
            else:
                continue
    f = open(db_root + 'names.txt', 'w')
    f.write(str(names))
    f = open(db_root + 'cuisines.txt', 'w')
    f.write(str(cuisines))
    f = open(db_root + 'locations.txt', 'w')
    f.write(str(locations))
    f = open(db_root + 'numbers.txt', 'w')
    f.write(str(numbers))
    f = open(db_root + 'prices.txt', 'w')
    f.write(str(prices))
    f = open(db_root + 'addresses.txt', 'w')
    f.write(str(addresses))
    f = open(db_root + 'post_codes.txt', 'w')
    f.write(str(post_codes))
    f = open(db_root + 'phones.txt', 'w')
    f.write(str(phones))
    f.close()

def load_entity_dict():
    f = open(db_root + 'names.txt', 'r')
    names = f.read()
    names = eval(names)
    f = open(db_root + 'cuisines.txt', 'r')
    cuisines = f.read()
    cuisines = eval(cuisines)
    f = open(db_root + 'locations.txt', 'r')
    locations = f.read()
    locations = eval(locations)
    f = open(db_root + 'sizes.txt', 'r')
    sizes = f.read()
    sizes = eval(sizes)
    f = open(db_root + 'prices.txt', 'r')
    prices = f.read()
    prices = eval(prices)
    f = open(db_root + 'phones.txt', 'r')
    phones = f.read()
    phones = eval(phones)
    f = open(db_root + 'post_codes.txt', 'r')
    post_codes = f.read()
    post_codes = eval(post_codes)
    api = ['api_call']
    f.close()
    return names, cuisines, locations, sizes, prices, phones, post_codes, api


def extract_entity(word):
    names, cuisines, locations, sizes, prices, phones, post_codes, api = load_entity_dict()
    if word in names:
        return '<name>'
    elif word in cuisines:
        return '<cuisine>'
    elif word in locations:
        return '<location>'
    elif word in sizes:
        return '<size>'
    elif word in prices:
        return '<price>'
    elif word in phones:
        return '<phone>'
    elif word in post_codes:
        return '<post_code>'
    elif word in api_call:
        return '<api>'
    else:
        return word


def build_candidate_dict(src_file, de, dst_root=db_root):
    candidate_dict = {}
    if de == True:
        with open(src_file) as src:
            lines = src.readlines()
            n_lines = len(lines)
            for i in range(n_lines):
                line = lines[i]
                line = line.strip().split(' ', 1)[1]
                words = line.split(' ')
                n_words = len(words)
                for j in range(n_words):
                    word = words[j]
                    entity = extract_entity(word)
                    if entity != word:
                        words[j] = entity
                line = ' '.join(words)
                if line not in candidate_dict.keys():
                    candidate_dict[line] = len(candidate_dict)
        f = open(dst_root + f_candidate_dict_de_name, 'w')
        f.write(str(candidate_dict))
        f.close()
    else:
        with open(src_file) as src:
            lines = src.readlines()
            n_lines = len(lines)
            for i in range(n_lines):
                line = lines[i]
                line = line.strip().split(' ', 1)[1]
                if line not in candidate_dict.keys():
                    candidate_dict[line] = len(candidate_dict)
        f = open(dst_root + f_candidate_dict_le_name, 'w')
        f.write(str(candidate_dict))
        f.close()
    return candidate_dict


def get_candidate_dict(de=True):
    src_file = f_candidate_dict_name
    try:
        f = open(db_root + src_file, 'r')
        candidate_dict = f.read()
        candidate_dict = eval(candidate_dict)
        f.close()
        return candidate_dict
    except:
        return build_candidate_dict(data_root + f_raw_candidates_name, de)
