import cv2 as cv
import numpy as np

def crop(image, x1, x2, y1, y2):
    #Will crop an numpy array from row y1 to row y2 and column x1 to x2.
    #crop(image, 0, 100, 0, 100) will give the top 100 pixels in both dimensions
    return np.uint8(image[y1:y2,x1:x2])

def crop_p(image, x1, y1, proportionx, proportiony):
    #Will crop a portion of the image
    if proportionx > 1 or proportiony > 1:
        print('proportion argument has to be between 0 and 1')
        return(image)
    elif proportionx <= 0 or proportiony <= 0:
        print('Cannot return 0 or a negative picture, choose a proportion argument between 0 and 1')
        return(image)
    else:
        num_rows = np.shape(image)[0]
        y2=int(proportiony*num_rows)
        num_cols = np.shape(image)[1]
        x2=int(proportionx*num_cols)
    while y2 < num_rows and x2 < num_cols:
        return np.uint8(image[y1:y2,x1:x2])
    print('Some portions of image outside range. Choose a smaller proportion or starting pixel')
    return(image)

def equalisation(image):
    #Will equalize the spectrum of pixels, giving the picture better contrast

    num_rows = np.shape(image)[0]
    num_cols = np.shape(image)[1]
    num_pixels = num_rows*num_cols

    #Memory allocation and defining variables
    eq_img = np.uint8(np.zeros((num_rows,num_cols)))
    freq=[0]*256 #frequency of a value
    prob=[0]*256 #probability of it having that value
    cumulative=0 #Used to calculate the cumulative probabilities
    cdp=[0]*256 #Cumulatiive distribution probabilities

    for row in image: #Goes through each row in the numpy array
        for val in row: #Goes through each value in the row
            freq[val-1]+=1 #Will give the number of times a specific pixel-value can be found in the picture

    for i in range(256):
        prob[i]=freq[i]/num_pixels #Gives the probability of a pixel having that value
        cumulative+=prob[i] #Gives the cumulative probability, meaning the probability of the pixel having that value or lower
        cdp[i]=round(cumulative*256) #Gives the convertion schema for each pixel value

    for i in range(num_rows):
        for j in range(num_cols):
            val_index=image[i,j]-1
            eq_img[i,j]=cdp[val_index] #Recalculates the new pixels

    return eq_img

def edge(image):
    #Will detect edges in a picture
    num_rows = np.shape(image)[0]
    num_cols = np.shape(image)[1]
    #Memory allocation and defining variables
    edges_img = np.uint8(np.zeros((num_rows,num_cols)))
    edges_window = np.zeros((3,3))
    weights = np.array([(1,1,1),(1,-8,1),(1,1,1)], dtype=int)

    for i in range(num_rows):
        for j in range(num_cols):
            convolution_window = image[i-1:i+2,j-1:j+2] #Gives the values to convolute on, see this as a square moving around on the image
            if np.shape(convolution_window)[0] < 3 or np.shape(convolution_window)[1] < 3: #If the convolution_window doesn't fit, on the borders
                edges_img[i,j]+=0 #Make these pixels black. This will mean we will get a 2pixel border of black pixels
            else: #If the entire convolution window fits inside the image
                edges_window =  np.multiply(convolution_window, weights) #Multiply each value in the convolution window with the corresponding weights
                mean = np.uint8(np.mean(edges_window)) #Calculate the mean value for the weighted convolution window
                edges_img[i,j]+=mean

    return(edges_img)

def blur(image, amount):
    #Will blur a picture by a given amount. Amount should be a int bigger than 0.
    num_rows = np.shape(image)[0]
    num_cols = np.shape(image)[1]
    #Memory allocation
    smoothed_img = np.uint8(np.zeros((num_rows,num_cols)))

    c_range = int(amount/2) #This is half the length of the convolution window

    for i in range(num_rows):
        for j in range(num_cols):
            convolution_window = image[i-c_range:i+c_range+1,j-c_range:j+c_range+1] #Define the convolution window based on the input
            if np.shape(convolution_window)[0] < amount or np.shape(convolution_window)[1] < amount: #If convolution window doesn't fit inside image
                smoothed_img[i,j]+=image[i,j] #Do nothing
            else:
                mean=np.uint8(np.mean(convolution_window)) #Calculate the mean value of the convolution window
                smoothed_img[i,j]+=mean #Add mean value to new image

    return(smoothed_img)
