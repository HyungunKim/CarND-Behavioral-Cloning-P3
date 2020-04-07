# **Behavioral Cloning** 

## Writeup

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./out_img/model_overview.png "Model Visualization"
[image2]: ./out_img/Warp0.PNG "Warp image 0"
[image3]: ./out_img/hybrid_drive_strategy.png "Hybrid drive strategy"
[image4]: ./out_img/view1.png "road_img"
[image5]: ./out_img/bird_eye_view1.png "Bird eye view"
[image6]: ./out_img/input1_flipped.png "Normal Image"
[image7]: ./out_img/decoded.png "Decoded Image"
[image8]: ./out_img/validation_result.png "Validation result"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
  
**Also includes hacky codes to use different computers for running the simulator and neural network which I call hybrid strategy.**

![Hybrid strategy][image3]
* model.ipynb to show working codes  
* model.html to show ipynb in html format.    
* hybrid_drive_unity_v2.py  
Sends image data from unity simulator and receives steering angle from hybrid_drive_server.
  
* hybrid_drive_server_v5.py  
Receives image from hybrid_drive_unity, steering angle from human tutor when training.  
Starts training loop when human tutor finished providing training data.
When it's allowed to drive, it calls trained network to figure out the steering angle from received image.  
Finally it sends out steering angle to hybrid_drive_unity (Whether or not this steering angle is calculated or provided from human tutor).
  
* human_tutor_v3.py  
Smooths out keyboard input.  
Send steering angle to the server when training.  
Signals server to update model parameters based on human input.  
This helps to efficiently gather training data where the neural network fails
  
* writeup_report.md
* `/model_check_points` containing all trained subnetworks.
  
Unfortunately I couldn't save my model in 1 `.h5` file.  
The model is of `tensorflow.keras.Model` class and it had some issues in saving the model.  
Each Part of the model had to be saved individually in `./model_check_points`. But I've provided a method to save and load these checkpoints.

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track.  
Type below on the computer running the simulation.  
```sh
python drive.py model_check_points

```  

Also to use different machine for simulating and predicting and to keep human tutor in the loop...  
(This also makes possible to use PI controller during training drives.)  
on the machine that has neural net  
```sh
pytohn hybrid_drive_server.py model_check_points
```

On the machine that runs simulation.
```sh
pytohn hybrid_drive_unity.py SERVER_IP:PORT
```

Tutor machine (need to be a window machine)  
```sh
pytohn human_tutor.py SERVER_IP:PORT
```

**notice Tutor machine uses [djnugent/CapnCtrl](https://github.com/djnugent/CapnCtrl)**  

Keep pressing `E` on the tutor's keyboard to send image to the model and update steering angle.  
press `Q` to take over control of the car.  
`A` or `D` key to smoothly steer left or right respectively.  
Keep pressing `Q` to smoothly restore steering to 0.  
When you are in control, every time you press any key (except `E, W, S`) it records your steering angle to make sampling efficient.  
i.e. you only press key (record) in situation where the neural network has to watch out for.  

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network.   
It is use `tensorflow 2.1` but the core model is subclass of `tensorflow.keras.Model`. Thus it's still `Keras` in a way.  
The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed
![Model overview][image1]

My model consists of a convolution neural network and fully connected neural network.  
Convolution layers have 3x3 filter sizes and depths between 16 and 64 (model.py lines 58-110)  
Fully connected layers have output shape of 256 if it is a hidden layer or 1 if it is the final output layer.

The model includes RELU layers to introduce nonlinearity, and the data is normalized before calling the network. (model.py line 171). 

#### 2. Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting (model.py lines 105, 107).  
Also all the convolutional layers have L2 parameter normalization.  

The model was trained and validated on a data sets that I've drove the track backwards to ensure that the model was not overfitting .  

The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. model parameter tuning

The model used an adam optimizer. It's `lr` parameter is set to a small value of 0.001 to ensure it atleast finds local minimum. (model.py line 162)  
I've actually tried to down size the input images and the model it self to make up for all additional delays between sensing and predicting. (I used two machine to send data back and forth).  
But luckly the internet very fast, it could at least get up to 10 fps (image sending by simulator and network replying its prediction)
Other than that there wasn't much to tune as the model drove the track very nicely.

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used `hybrid_drive` strategy to make good use of PI controller.   
First I've recorded my drive with `set_speed = 4` so that I can focus on what steering angle I should give.  
Later it turned out my model worked only when it drived at speed 4!  
Thus I've re recorded my drive with same `set_speed` as the model's (i.e. 9mph)  

I've 1 lap of driving, trained it, and captured few more points where the model actually did terrible.  
I guess this gave me a big boost data efficiency.  

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to extract useful features with encoder-decoder model.  

![Bird eye view][image2]

I've trained encoder-decoder model to regenerate original bird-eye view input.(model.ipynb In [14])  
![Bird eye view][image6]
![Auto encoder output][image7]
This is helpful as encoder part of the model gets more training experience.  

Next the predict part of the model has convolutional part and fully connected part.  
As the encoder tries to preserve the contents of the original image, I've created another convolutional layer that focuse entirely on getting the steering angle right. (predict conv)  
Finally features extracted from convolutional layer is given to a dense layer to predict steering angle.  

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set.   
Training set consists of 1 laps in counter clockwise direction 
My training set was made with 2 machines using `hybrid_drive_server`, `hybrid_drive_unity`, `human_tutor`.  
Validation data consists 1 laps clockwise direciton with all left, center, right camera images.  
Thus my validation set is made from normal `training mod` of udacity simulator, but I've tried to drive as close to 9mph as possible.

To combat the overfitting, I modified the model so that it had drop out on the fully connected layers, kernel regularization on all the convolutional layers.  

During the training loop I've randomly flipped the image and the sign of the steering angle.  

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track consistently.  
I've took over where the model failed horribly and captured how to handle this scenario (whith exagerated steering) and retrained the model with this data included.  

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

![Model overview][image1]  

The final model architecture (model.py lines 58-108) details are listed below.

```
Model: Encoder
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 160, 320, 16)      448       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 80, 160, 16)       0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 80, 160, 32)       4640      
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 40, 80, 32)        0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 40, 80, 32)        9248      
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 20, 40, 32)        0         
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 20, 40, 64)        18496     
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 10, 20, 64)        0         
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 10, 20, 64)        36928     
_________________________________________________________________
max_pooling2d_4 (MaxPooling2 (None, 5, 10, 64)         0         
=================================================================
Total params: 69,760
Trainable params: 69,760
Non-trainable params: 0
_____________________________
```
```
Model: Decoder
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
up_sampling2d (UpSampling2D) (None, None, None, 64)    0         
_________________________________________________________________
conv2d_5 (Conv2D)            (None, None, None, 64)    36928     
_________________________________________________________________
up_sampling2d_1 (UpSampling2 (None, None, None, 64)    0         
_________________________________________________________________
conv2d_6 (Conv2D)            (None, None, None, 64)    36928     
_________________________________________________________________
up_sampling2d_2 (UpSampling2 (None, None, None, 64)    0         
_________________________________________________________________
conv2d_7 (Conv2D)            (None, None, None, 32)    18464     
_________________________________________________________________
up_sampling2d_3 (UpSampling2 (None, None, None, 32)    0         
_________________________________________________________________
conv2d_8 (Conv2D)            (None, None, None, 32)    9248      
_________________________________________________________________
up_sampling2d_4 (UpSampling2 (None, None, None, 32)    0         
_________________________________________________________________
conv2d_9 (Conv2D)            (None, None, None, 3)     867       
=================================================================
Total params: 102,435
Trainable params: 102,435
Non-trainable params: 0
```
```
Model: predict_conv
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_5 (Conv2D)            (None, 5, 10, 64)         36928     
_________________________________________________________________
conv2d_6 (Conv2D)            (None, 5, 10, 64)         36928     
_________________________________________________________________
max_pooling2d_5 (MaxPooling2 (None, 2, 5, 64)          0         
_________________________________________________________________
conv2d_7 (Conv2D)            (None, 2, 5, 128)         73856     
_________________________________________________________________
conv2d_8 (Conv2D)            (None, 2, 5, 128)         147584    
_________________________________________________________________
global_max_pooling2d (Global (None, 128)               0         
=================================================================
Total params: 295,296
Trainable params: 295,296
Non-trainable params: 0
```
```
Model: predict (fully connected)
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
dense (Dense)                (None, 256)               33024     
_________________________________________________________________
dropout (Dropout)            (None, 256)               0         
_________________________________________________________________
dense_1 (Dense)              (None, 256)               65792     
_________________________________________________________________
dropout_1 (Dropout)          (None, 256)               0         
_________________________________________________________________
dense_2 (Dense)              (None, 1)                 257       
=================================================================
Total params: 99,073
Trainable params: 99,073
Non-trainable params: 0
```

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded one laps on track one using center lane driving using hybrid strategy. Here is an example image of center lane driving:

![alt text][image4]

I then recorded the vehicle recovering from places where the previous model failed and retrained with these data included.   

To augment the data sat, I also flipped images and angles thinking that this would ... For example, here is an image that has then been flipped:

![alt text][image5]
![alt text][image6]

Etc ....

After the collection process, I had 1176 number of data points. I then preprocessed this data by Warping to bird-eye view, and rescaleing (model.py line 171)

```
  Training data
	steering
count 	1176.000000
mean 	-0.047226
std 	0.103617
min 	-0.488173
25% 	-0.086111
50% 	-0.030634
75% 	-0.004934
max 	0.411923
```
Than I've recorded validation data in `Training mode` of the simulator.  
Drove one laps clockwise (opposite of training data) while trying to maintain 9 mph. 

```
  Validation data
	steering 	throttle 	break 	speed
count 	2797.000000 	2797.000000 	2797.0 	2797.000000
mean 	0.025964 	0.074298 	0.0 	9.065184
std 	0.088532 	0.082401 	0.0 	0.304721
min 	-0.424528 	0.000000 	0.0 	7.608748
25% 	-0.009434 	0.000000 	0.0 	8.876772
50% 	0.028302 	0.043154 	0.0 	9.034074
75% 	0.066038 	0.143944 	0.0 	9.194744
max 	0.301887 	0.331947 	0.0 	10.437590
```

It turned out my training data was smaller in size than my validation data.  
The training, validation result looked fantastic.(model.ipynb or model.html In[13], Out[13])  
![Validation result][image8]

My model was trained with very small dataset and even without left, right camera image.  
Yet it did so well on all camera image.

