import tensorflow as tf


def zero_nil_slot(t, name=None):
    with tf.op_scope([t], name, 'zero_nil_slot') as name:
        t = tf.convert_to_tensor(t, name='t')
        s = tf.shape(t)[1]
        z = tf.zeros(tf.stack([1, s]))
        return tf.concat(axis=0, values=[z, tf.slice(t, [1, 0], [-1, -1])], name=name)


class MemoryNetwork:
    def __init__(self, candidates_vector, batch_size, memory_size, sentence_size, candidate_size, vocabulary_size,
                 embedding_size=30,
                 hops=1, initializer=tf.random_normal_initializer(stddev=0.1), session=tf.Session(), index=0):
        self.index = index
        self.batch_size = batch_size
        self.memory_size = memory_size
        self.sentence_size = sentence_size
        self.candidate_size = candidate_size
        self.vocabulary_size = vocabulary_size
        self.embedding_size = embedding_size
        self.hops = hops
        self.initializer = initializer
        self.session = session
        self.name = 'MemoryNetwork'
        self.candidates = candidates_vector

        self.build_inputs()
        self.build_variables()
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
        self.session.run(tf.global_variables_initializer())
        logits = self.inference(self.context, self.utterances)
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,
                                                                       labels=tf.cast(self.responses, dtype=tf.int32),
                                                                       name='cross_entropy')
        cross_entropy_sum = tf.reduce_sum(cross_entropy, name='cross_entropy_sum')
        self.loss_op = cross_entropy_sum
        gradients_and_variables = self.optimizer.compute_gradients(self.loss_op)
        gradients_and_variables = [(tf.clip_by_norm(g, 40), v) for g, v in gradients_and_variables]
        nil_gradients_and_variables = []
        for g, v in gradients_and_variables:
            if v.name in self.nil_variables:
                nil_gradients_and_variables.append((zero_nil_slot(g), v))
            else:
                nil_gradients_and_variables.append((g, v))
        self.train_op = self.optimizer.apply_gradients(nil_gradients_and_variables, name='train_op')

        # self.train_op = self.optimizer.minimize(self.loss_op)
        self.predict_op = tf.argmax(logits, axis=1)
        self.saver = tf.train.Saver()

    def build_inputs(self):
        self.context = tf.placeholder(dtype=tf.int32, shape=[None, None, self.sentence_size], name='context')
        self.utterances = tf.placeholder(dtype=tf.int32, shape=[None, self.sentence_size], name='utterances')
        self.responses = tf.placeholder(dtype=tf.int32, shape=[None], name='responses')

    def build_variables(self):
        with tf.name_scope(self.name):
            nil_word_slot = tf.zeros([1, self.embedding_size])
            AC = tf.concat(values=[nil_word_slot, self.initializer([self.vocabulary_size - 1, self.embedding_size])],
                           axis=0)
            self.AC = tf.Variable(AC, name='A')
            self.H = tf.Variable(self.initializer([self.embedding_size, self.embedding_size]), name='H')
            W = tf.concat(values=[nil_word_slot, self.initializer([self.vocabulary_size - 1, self.embedding_size])],
                          axis=0)
            self.W = tf.Variable(W, name='W')
        self.nil_variables = set([self.AC.name, self.W.name])

    def print_variables(self):
        for x in self.AC:
            print(x.name, self.session.run(x))
        print(self.W.name, self.session.run(self.W))

    def inference(self, context, utterances):
        with tf.name_scope(self.name):
            utterances_embedding = tf.nn.embedding_lookup(self.AC, utterances)
            u_0 = tf.reduce_sum(utterances_embedding, 1)
            u = [u_0]
            for i in range(self.hops):
                memory_embedding = tf.nn.embedding_lookup(self.AC, context)
                memory_embedding = tf.reduce_sum(memory_embedding, 2)
                u_tmp = tf.transpose(tf.expand_dims(u[-1], -1), [0, 2, 1])
                dot_product = tf.reduce_sum(memory_embedding * u_tmp, 2)
                probabilities = tf.nn.softmax(dot_product)
                probabilities_tmp = tf.transpose(tf.expand_dims(probabilities, -1), [0, 2, 1])
                c_tmp = tf.transpose(memory_embedding, [0, 2, 1])
                o_k = tf.reduce_sum(c_tmp * probabilities_tmp, 2)
                u_k = tf.matmul(u[-1], self.H) + o_k
                u.append(u_k)
            candidates_embedding = tf.nn.embedding_lookup(self.W, self.candidates)
            candidates_embedding_sum = tf.reduce_sum(candidates_embedding, 1)
        return tf.matmul(u[-1], tf.transpose(candidates_embedding_sum))

    def batch_feed(self, context, utterances, responses):
        feed_dict = {self.context: context, self.utterances: utterances, self.responses: responses}
        loss, _ = self.session.run([self.loss_op, self.train_op], feed_dict=feed_dict)
        return loss

    def predict(self, context, utterances):
        feed_dict = {self.context: context, self.utterances: utterances}
        return self.session.run(self.predict_op, feed_dict=feed_dict)

    def save_model(self, dst_directory='models/'):
        save_path = dst_directory + 'model.ckpt'
        save_path = self.saver.save(self.session, save_path)
        data_dict = {'batch_size': self.batch_size, 'candidate_size': self.candidate_size,
                     'memory_size': self.memory_size, 'sentence_size': self.sentence_size,
                     'vocabulary_size': self.vocabulary_size, 'embedding_size': self.embedding_size, 'hops': self.hops}

        f = open('models/model-wiki.txt', 'w')
        f.write(str(data_dict))
        f.close()

    def load_model(self, src_file='models/model.ckpt'):
        saver = tf.train.Saver()
        saver.restore(self.session, src_file)

    def get_embedding(self, word_id):
        embedding = tf.nn.embedding_lookup(self.AC, word_id)
        return embedding
