# YouTube link: 

https://www.youtube.com/watch?v=uEnXdc9hvto


In this project, I built a neural network to classify road signs based on an image. I 
downloaded the German Traffic Sign Recognition Benchmark (GTSRB) dataset that has images of 43 signs and imported in the project.
 I implemented two functions load_data and get_model. The first function accepts an argument data_dir which is the path to the directory where the data is stored and returns a tuple (images, labels).
The seconds function get_model I built and return a compiled neural network model
It's quite common for computer vision to build a convolutional neural network. For the implementation of the network the Keras Api was used that supplies an easier interface to the famous TensorFlow platform.
Below I describe the first model in detail and afterwards other models that I test in the effort to find the one with the best results. 

# First model

Starting the configuration of the model I selected the model to be sequential. This means that the output on one layer is the output of the next layer. 
The first layer added was a convolution layer with 32 filters in the feature map. The kernel had a size of (3,3). Kernal is like a sliding widow that the convolution layer uses to learn. For activation "relu" (Rectified Linear unit) was used. A common and fast solution. The Input shape was equal to (IMG_WIDTH, IMG_HEIGHT, 3), meaning the image width, the image height, and the 3 values for each pixel for red, green, and blue.
After each convolution layer the dimensionality increases as the possibility for overfitting as the model learns the training data. For that reason, a pooling layer is often following a convolution layer. So, a max-pooling layer was used of a 2x2 pool size. This means that from that 2x2 pool size we kept the maximum value. 
Afterwards another convolutional layer and pooling layer were added, with the same configuration,  to get more information and then reduce dimensionality. A Kera's flatten layer is added to transform the input to one dimension. It is followed by a dense layer that has 128 units and a “relu” activation. A dropout layer is added to avoid overfitting by removing certain nodes during training.
Lastly, an output layer with output units for all 43 units. The "softmax" activation function produced a normalized probability distribution for the given image being each type of road sign.
Finally, the compile method of the model is called with the following parameters:
For the optimizer, the "adam" algorithm was selected. It is a classical stochastic gradient descent procedure to update network weights iterative based on training data. For the loss parameter. For the loss parameter I passed “categorical_crossentropy”. This is a loss function for multi-class classification model where there are two or more output labels.  As a metric, the value that will be produced to evaluate the model, accuracy was selected.
The result of this model was the following:
loss: 0.1716 - accuracy: 0.9526

# Second model
Although the result was satisfactory enough modifying the hyperparameters  could possibly get better results. For the second model  the  convolution layers filters were increased to 64 keeping the same kernel size. No other parameter was modified. The result was the following:
loss: 0.2224 - accuracy: 0.9408

# Third model
This time I increased the size of the kernel for the  convolution layers filters from(3,3) to (4,4). Every other parameter to every other layer was kept the same. The result was  very good:
loss: 0.1627 - accuracy: 0.9645
That was finally the best result I had and the model that was selected.

# Fourth model
The enemy of the good is the perfect, so a fourth model was tested.  In the second model the doubling of the convolution layers filters improved the accuracy, so I doubled them again to 128  but returned the kernel size to (3,3). Moreover, I doubled the dense layer from 128 to 256.
The result the following:
loss: 0.3141 - accuracy: 0.9200

# Fifth Model
Finally, I tried to get the best model the third and just change a parameter to see if I could get a better result.  The convolutional layer filters are back to 64 with kernel size of (4,4). The max-pooling layers are kept to  2x2 size. The change was that the dense layer size increased to 256. The results were not so good:
loss: 0.3542 - accuracy: 0.9123

The best model was  the third.

# Usage
Download the data set  unzip it. Move the resulting gtsrb directory inside the traffic directory.
Inside of the traffic directory, run pip3 install -r requirements.txt to install this project’s dependencies: opencv-python for image processing, scikit-learn for ML-related functions, and tensorflow for neural networks.

To run the program, enter python traffic.py gtsrb at the console.  (gtsrb is the directory with the data).





