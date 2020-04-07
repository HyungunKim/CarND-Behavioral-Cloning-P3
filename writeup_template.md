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

[image1]: ./images/model_overview.png "Model Visualization"
[image2]: ./examples/placeholder.png "Grayscaling"
[image3]: ./examples/placeholder_small.png "Recovery Image"
[image4]: ./examples/placeholder_small.png "Recovery Image"
[image5]: ./examples/placeholder_small.png "Recovery Image"
[image6]: ./examples/placeholder_small.png "Normal Image"
[image7]: ./examples/placeholder_small.png "Flipped Image"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
  
**Also includes hacky codes to use different computers for running the simulator and neural network.**
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
This helps to efficiently gather training data where the network fails
  
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
![alt text][image1]

My model consists of a convolution neural network and fully connected neural network.  
Convolution layers have 3x3 filter sizes and depths between 16 and 64 (model.py lines 58-110)  
Fully connected layers have output shape of 256 if it is a hidden layer or 1 if it is the final output layer.

The model includes RELU layers to introduce nonlinearity, and the data is normalized before calling the network. (model.py line 171). 

#### 2. Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting (model.py lines 105, 107).  
Also all the convolutional layers have L2 parameter normalization.  

The model was trained and validated on a data sets that i've drove the track backwards to ensure that the model was not overfitting .  

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

I've trained encoder-decoder model to regenerate original bird-eye view input.  
This is helpful as encoder part of the model gets more training experience.  

Next the predict part of the model has convolutional part and fully connected part.  
As the encoder tries to preserve the contents of the original image, I've created another convolutional layer that focuse entirely on getting the steering angle right. (predict conv)

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set.   
My training set was made with 2 machines using `hybrid_drive_server`, `hybrid_drive_unity`, `human_tutor`.  
It consist of 

To combat the overfitting, I modified the model so that ...

Then I ... 

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track... to improve the driving behavior in these cases, I ....

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture (model.py lines 18-24) consisted of a convolution neural network with the following layers and layer sizes ...

Here is a visualization of the architecture (note: visualizing the architecture is optional according to the project rubric)

![alt text][image1]

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving. Here is an example image of center lane driving:

![alt text][image2]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would learn to .... These images show what a recovery looks like starting from ... :

![alt text][image3]
![alt text][image4]
![alt text][image5]

Then I repeated this process on track two in order to get more data points.

To augment the data sat, I also flipped images and angles thinking that this would ... For example, here is an image that has then been flipped:

![alt text][image6]
![alt text][image7]

Etc ....

After the collection process, I had X number of data points. I then preprocessed this data by ...


I finally randomly shuffled the data set and put Y% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was Z as evidenced by ... I used an adam optimizer so that manually training the learning rate wasn't necessary.
