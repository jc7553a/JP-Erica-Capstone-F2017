import tensorflow as tf
import numpy as np

class MLP(object):

    '''Template MultiLayer Perceptron Class'''
    '''The output right now is 2 Values'''
    '''I think you should try to reduce a mean value hence 2 ouput values'''

    def __init__(self, n_features, n_hidden):
        '''Number of Inputs and Number of Hidden units'''
        ''' One Hidden Layer in this Network'''
        self.n_features = n_features
        self.n_hidden = n_hidden
        #self.transfer = transfer_function

        network_weights = self._initialize_weights()
        self.weights = network_weights

        # model
        self.x = tf.placeholder(tf.float32, [None, self.n_features])
        self.y = tf.placeholder(tf.float32, [None,2])
        self.hidden = tf.nn.sigmoid(tf.add(tf.matmul(self.x, self.weights['w1']), self.weights['b1']))
        self.finish = tf.add(tf.matmul(self.hidden, self.weights['w2']), self.weights['b2'])

        # cost
        self.cost = tf.reduce_mean(tf.square(self.finish - self.y))
        self.optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(self.cost)

        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)
        'Uncomment to Look at Graph and Nodes'
        #print(tf.get_default_graph().as_graph_def())


    def _initialize_weights(self):
        all_weights = dict()
        all_weights['w1'] = tf.Variable(tf.truncated_normal([self.n_features, self.n_hidden], stddev = .001), name = 'weights1')
        all_weights['b1'] = tf.Variable(tf.truncated_normal([self.n_hidden], stddev = .001), name = 'bias1')
        all_weights['w2'] = tf.Variable(tf.truncated_normal([self.n_hidden, 2], stddev = .001), name = 'weights_o')
        all_weights['b2'] = tf.Variable(tf.truncated_normal([2], stddev = .001), name = 'biases_o')
        return all_weights

    def train(self, X, Y):
        cost, opt = self.sess.run((self.cost, self.optimizer), feed_dict={self.x: X, self.y: Y})
        return cost

    def calc_total_cost(self, X, Y):
        return self.sess.run(self.cost, feed_dict = {self.x: X, self.y: Y})

    def transform(self, X):
        return self.sess.run(self.hidden, feed_dict={self.x: X})

    def generate(self, hidden = None):
        if hidden is None:
            hidden = self.sess.run(tf.random_normal([1, self.n_hidden]))
        return self.sess.run(self.output, feed_dict={self.hidden: hidden})

    def output(self, X):
        return self.sess.run(self.finish, feed_dict={self.x: X})

    def getWeights(self):
        return self.sess.run(self.weights['w1'])

    def getBiases(self):
        return self.sess.run(self.weights['b1'])
    
    def getHiddenWeights(self):
        return self.sess.run(self.weights['w2'])
    
    def getHiddenBiases(self):
        return self.sess.run(self.weights['b2'])

    'Uncomment to Look at Graph and Nodes'
    #print(tf.get_default_graph().as_graph_def())
