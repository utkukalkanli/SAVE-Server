## Facial Expression Recognition

This repository features a python script which is able to recognize your facial expression using a webcam or some other camera attached to a computer.
Training data consists of 48x48 pixel grayscale images of faces. The objective is to classify each face based on the emotion shown in the facial expression into one of seven categories (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral). In this project OpenCV was used to automatically detect faces in images and draw bounding boxes around them. Once we had trained, saved, and exported the CNN, we directly served the trained model to a web interface and perform real-time facial expression recognition on video and image data. For serverizing the application, Flask was used.

![Alt text](./model.png)


## References

https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data
