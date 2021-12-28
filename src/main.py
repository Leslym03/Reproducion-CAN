import tensorflow as tf
from DCGAN import *
from CAN import *

def main(_):
    run_config = tf.ConfigProto()
    run_config.gpu_options.allow_growth=True

    with tf.Session(config=run_config) as sess:
        can = CAN(sess)
        can.build_model()
        can.train()

        dcgan = DCGAN(sess)
        dcgan.build_model()
        dcgan.train()

if __name__ == '__main__':
    tf.app.run()