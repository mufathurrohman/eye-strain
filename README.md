# Avoiding Computer Vision Syndrome
This app will remind you to take a break for every 20 minutes using [Facial Landmarks](https://towardsdatascience.com/facial-mapping-landmarks-with-dlib-python-160abcf7d672) and [Eye Aspect Ratio Calculation](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/). The 20 minutes interval is taken from [20-20-20](https://www.medicalnewstoday.com/articles/321536) rule (20 minutes spent @screen -> look at something 20 feet away for 20 seconds). Normally, a person will blink between 10-15 times per minutes (Blehm et al., 2005).  

Blehm, C., Vishnu, S., Khattak, A., Mitra, S., and Yee, R. W. (2005). Computer Vision Syndrome: A Review. Survey of Opthalmology, 50, 253–262.


### Requirements
1. Windows 10
2. Python 3.6 
3. Webcam
4. shape_predictor_68_face_landmarks.dat (download from [here](https://github.com/italojs/facial-landmarks-recognition-/blob/master/shape_predictor_68_face_landmarks.dat))

### Dependencies
1. OpenCV2
2. dlib
3. imutils
4. numpy
5. scipy
6. win10toast
 
### Additional Info
- To close the app, press `Esc`

#### Eye Landmarks
Detected eyes will be marked by green dots.
![Marked Eyes](https://github.com/mufathurrohman/eye-strain/blob/master/eye-landmarks.PNG)

#### The Notification
The notification should disappear after 5 seconds.
![Toast](https://github.com/mufathurrohman/eye-strain/blob/master/toast.PNG)

#### Blink Summary
Will be available as `Blink Summary.txt` after the user closes the app.
![Notification](https://github.com/mufathurrohman/eye-strain/blob/master/blink%20summary.PNG)
