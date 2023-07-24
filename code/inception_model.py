# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Contains a variant of the CIFAR-10 model definition."""


import torch 
import torch.nn as nn 
import torch.nn.functional as F

def truncated_normal(stddev): 
  return torch.nn.init.normal_(torch.empty(stddev.size()), mean = 0, std = stddev)

class CifarNet(nn.Module): 
  def __init__(self, num_classes = 10, dropout_keep_prob = 0.5): 
    super(CifarNet, self).__init__()
    self.num_classes = num_classes
    self.dropout_keep_prob = dropout_keep_prob
    self.conv1 = nn.Conv2d(in_channels = 3, out_channels = 64, kernel_size = 5, stride = 1, padding = 2)
    self.conv2 = nn.Conv2d(in_channels = 64, out_channels = 64, kernel_size = 5, stride = 1, padding = 2) 
    self.pool1 = nn.MaxPool2d(kernel_size = 2, stride = 2)
    self.pool2 = nn.MaxPool2d(kernel_size = 2, stride = 2)
    self.norm1 = nn.LocalResponseNorm(size = 4, alpha = 0.001/9.0, beta = 0.75, k=1.0)
    self.norm2 = nn.LocalResponseNorm(size = 4, alpha = 0.001/9.0, beta = 0.75, k = 1.0)
    self.fc3 = nn.Linear(8*8*64, 384)
    self.fc4 = nn.Linear(384,192)
    self.logits = nn.Linear(192, num_classes)
    self.dropout3 = nn.Dropout(p=1 - self.dropout_keep_prob)

  """Creates a variant of the CifarNet model.

  Note that since the output is a set of 'logits', the values fall in the
  interval of (-infinity, infinity). Consequently, to convert the outputs to a
  probability distribution over the characters, one will need to convert them
  using the softmax function:

        logits = cifarnet.cifarnet(images, is_training=False)
        probabilities = tf.nn.softmax(logits)
        predictions = tf.argmax(logits, 1)

  Args:
    images: A batch of `Tensors` of size [batch_size, height, width, channels].
    num_classes: the number of classes in the dataset.
    is_training: specifies whether or not we're currently training the model.
      This variable will determine the behaviour of the dropout layer.
    dropout_keep_prob: the percentage of activation values that are retained.
    prediction_fn: a function to get predictions out of logits.
    scope: Optional variable_scope.

  Returns:
    logits: the pre-softmax activations, a tensor of size
      [batch_size, `num_classes`]
    end_points: a dictionary from components of the network to the corresponding
      activation.
  """
 

# Turn on if the batch norm is used.
#   batch_norm_params = {
#     # Decay for the moving averages.
#     'decay': 0.9997,
#     # epsilon to prevent 0s in variance.
#     'epsilon': 0.001,
#     # collection containing the moving mean and moving variance.
#     #'moving_vars': 'moving_vars',
#   }

#   with slim.arg_scope([slim.conv2d, slim.fully_connected],
#                          normalizer_params=batch_norm_params,
#                          normalizer_fn=slim.batch_norm):
def forward(self, x): 
  #first
  x = F.relu(self.conv1(x))
  x = self.pool1(x)
  x = self.norm1(x)
  end_points = {'conv1':x}
#second 
  x = F.relu(self.conv2(x))
  x = self.pool2(x)
  x = self.norm2(x)
  end_points['conv2'] = x
#flatten
  x = torch.flatten(x,1)
  end_points['Flatten'] = x

  return logits, end_points 
cifarnet.default_image_size = 32


def cifarnet_arg_scope(weight_decay=0.004):
  """Defines the default cifarnet argument scope.

  Args:
    weight_decay: The weight decay to use for regularizing the model.

  Returns:
    An `arg_scope` to use for the inception v3 model.
  """
  with slim.arg_scope(
      [slim.conv2d],
      weights_initializer=tf.truncated_normal_initializer(stddev=5e-2),
      activation_fn=tf.nn.relu):
    with slim.arg_scope(
        [slim.fully_connected],
        biases_initializer=tf.constant_initializer(0.1),
        weights_initializer=trunc_normal(0.04),
        weights_regularizer=slim.l2_regularizer(weight_decay),
        activation_fn=tf.nn.relu) as sc:
      return sc
