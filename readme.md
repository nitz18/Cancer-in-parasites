## Simulated fake parasitic microorganism images and dye sensor images. Used efficient data structures to store the images. Used both the images to check if the parasite has cancer 

### 1. Efficient data structure to store microscope and dye sensor images 

- Microscope Image 

The microscope image consists of a microorganism which shows up as a single blob of arbitrary shape. In the worst case if the image has black and white pixels alternatively, then a 16 bit grayscale image would require 2 bytes per pixel x 100,000 x 100,000 which is 20 GB to store an image. An 8 bit grayscale image would require 1 byte per pixel x 100,000 x 100,000 which is 10 GB to store an image. Assuming that each image is a binary image that has only two possible values 0 for black and is a part of the blob. 1 for white and is not a part of the blob. Hence, 1 bit per pixel x 100,000 x 100,000 which is 1.25 GB. For a general case, we assume that the blob is convex in shape which means that we can store only the start index and the end index of the blob in each row, then a 32 bit grayscale image would require 3 bytes per pixel x 100,000 rows x 2(start index and end index) which is 0.6 MB. 

To implement this programmatically, we can use a dictionary. Where we store the row number as the key, followed by the start index and the end index of the blob in each row as the values. 

Example: 

|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| - | - | - | - | - | - | - | - | - | - | - |
|0  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
|1  |0 |0 |1 |1 |1 |1 |1 |1 |1 |1
|2  |0 |0 |0 |0 |1 |1 |1 |1 |0 |0| 
|3  |0 |0 |0 |0 |1 |1 |1 |1 |1 |1| 
|4  |0 |0 |0 |0 |0 |0 |0 |0 |0 |0| 

This can be stored as {0:[6,9],1:[2,9],2:[4,7],3:[4,9]}

- Dye Sensor 

In the case of the dye sensor image, we cannot store only the start and the end index as the dye flows through different parts of the blob. There is also leakage which means that the dye flows outside the parasite. Hence, in this case each pixel can be stored as 1 bit. 1 bit per pixel x 100,000 x 100,000 which is 1.25 GB to store an image. Also, it is expected that fewer than 0.1% of the parasites will have cancer and the researchers would like to store images only for those parasites that have cancer. Hence the storage space required will decrease futher. 

### 2. Creating “fake” simulated images

To make the images realistic, I used the make blob function which creates a 2D blob using numpy normal distribution function and smoothens the data by applying a Gaussian filter. For the dye sensor image, I filled several vertical strips and diagonals with 0s. 

Simulated parasite 

![Unknown-3](https://user-images.githubusercontent.com/98286997/163927274-257b20ba-a2a5-4904-ba13-4294f9aa41b3.png)

Simulated dye sensor image

![Unknown-2](https://user-images.githubusercontent.com/98286997/163927297-05f33130-67f7-4bb9-93f8-38ff03ec5265.png)


### 3. Cancer detection 

The cancer detection function predicts if the parasite has cancer by dividing the area occupied by the parasite in the image by the area occupied by the dye inside the parasite. This function also reconstructs the image using the dictionary. 

Reconstructing the parasite image from the dictionary 

![Unknown](https://user-images.githubusercontent.com/98286997/163927385-539ebf2a-ed78-4814-8a35-3c4ac8a9df16.png)


### 4. Improving the execution speed

To improve the execution speed, the enitre image does not have to be reconstructed. Using the start and the end indices the area of the parasite and the area of the dye inside the parasite can be calculated. 
The execution time to find if the parasite has cancer by constructing the image takes 1.29 seconds but the execution time to find if the parasite has cancer without constructing the image takes only 0.3 seconds. 
 
