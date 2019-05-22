from utils.arguments import task_id, de
from utils.data_utils import vocabulary, candidate_dict, candidates_vector
from utils.data_utils import memory_max_size, sentence_max_size, candidate_max_size
from utils.data_utils import vectorize_sentence, next
from sklearn.model_selection import train_test_split
from models.memory_network import MemoryNetwork
import numpy as np
import tensorflow as tf
from sklearn import metrics
from datetime import datetime

print('IN main_trn')

utils_root = 'utils/'
f_data_trn_name = 'data-trn{}-{}.txt'.format(task_id, 'de' if de == True else 'le')
f_data_tst_name = 'data-tst{}-{}.txt'.format(task_id, 'de' if de == True else 'le')
tf.flags.DEFINE_float('learning_rate', 0.01, '')
tf.flags.DEFINE_integer('epochs', 200, '')
tf.flags.DEFINE_integer('batch_size', 32, '')
tf.flags.DEFINE_integer('embedding_size', 30, '')
tf.flags.DEFINE_integer('hops', 3, '')
FLAGS = tf.flags.FLAGS
n_candidate = len(candidate_dict)
n_vocabulary = len(vocabulary.keys())
arg = 'learning_rate = ' + str(FLAGS.learning_rate) + '\n' \
    + 'epochs = ' + str(FLAGS.epochs) + '\n' \
    + 'batch_size = ' + str(FLAGS.batch_size) + '\n' \
    + 'embedding_size = ' + str(FLAGS.embedding_size) + '\n' \
    + 'hops = ' + str(FLAGS.hops) + '\n'
print(arg)

print('PREPARE DATA')
f_data_trn = open(utils_root + f_data_trn_name, 'r')
data_trn = next(f_data_trn, 1000000)
f_data_tst = open(utils_root + f_data_tst_name, 'r')
data_tst = next(f_data_tst, 1000000)
data = data_trn + data_tst
data_trn, data_tst = train_test_split(data, test_size=0.4)
trainC = []
trainU = []
trainR = []
for data_item in data_trn:
    (c, u, r) = data_item
    trainC.append(np.array(c))
    trainU.append(np.array(u))
    trainR.append(np.array(r))
testC = []
testU = []
testR = []
for data_item in data_tst:
    (c, u, r) = data_item
    testC.append(np.array(c))
    testU.append(np.array(u))
    testR.append(np.array(r))
n_train = len(data_trn)
n_test = len(data_tst)
batches = zip(range(0, n_train - FLAGS.batch_size, FLAGS.batch_size),
              range(FLAGS.batch_size, n_train, FLAGS.batch_size))
batches = [(start, end) for start, end in batches]
loss = []

print('START TRAINING', 'Training Size=' + str(n_train), 'Testing Size=' + str(n_test), sep='\n')
with tf.Session() as session:
    model = MemoryNetwork(candidates_vector, FLAGS.batch_size, memory_max_size, sentence_max_size,
                          candidate_max_size, n_vocabulary, embedding_size=FLAGS.embedding_size, hops=FLAGS.hops,
                          session=session)
    log = open('log_{}.txt'.format(datetime.now()), 'w')
    s = 'task_id = ' + str(task_id) + '\n' + 'de = ' + str(de) + '\n' + 'Training Size = ' + str(
        n_train) + '\n' + 'Testing Size = ' + str(n_test) + '\n' + 'Candidate Size = ' + str(n_candidate) + '\n'
    log.write(s)
    for t in range(1, FLAGS.epochs + 1):
        np.random.shuffle(batches)
        total_cost = 0.0
        for start, end in batches:
            c = np.array(trainC[start:end])
            u = np.array(trainU[start:end])
            r = np.array(trainR[start:end])
            cost = model.batch_feed(c, u, r)
            total_cost = total_cost + cost
        loss.append(total_cost)
        print(total_cost)
        if t % 5 == 0:
            train_predictions = model.predict(trainC, trainU)
            test_predictions = model.predict(testC, testU)
            train_accuracy = metrics.accuracy_score(np.array(train_predictions), trainR)
            test_accuracy = metrics.accuracy_score(np.array(test_predictions), testR)

            data = '---------------------' + '\n' \
                   + 'Epoch' + ' ' + str(t) + '\n' \
                   + 'Total Cost' + ' ' + str(total_cost) + '\n' \
                   + 'Train Accuracy' + ' ' + str(train_accuracy) + '\n' \
                   + 'Test Accuracy' + ' ' + str(test_accuracy) + '\n' \
                   + '---------------------' + '\n'
            print(data)
            log.write(data)
    log.write(str(loss))
    log.close()
    model.save_model()
print('DONE')
