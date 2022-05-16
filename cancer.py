#necessary imports 
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import io
from PIL import Image
import time

class DragonFruit:
    def __init__(self):
        pass 
    
    def make_blob(self):

        """ the make blob function creates a 2D blob using numpy distribution function 
        and smoothens the data by applying a Gaussian filter 
        returns 
            arr_01 array containing 0s and 1s"""

        #(mean) where the peak exists
        value= 50
        #(standard deviation) how flat the graph distribution should be
        scale= 20 
        #the shape of the returned array
        size= 30 
        #standard deviation for Gaussian kernel
        sigma= 2
        np.random.seed(60)

        #generating normally distributed values 
        r = np.random.normal(value, scale, size=size)    
        #generating theta values to use for cos and sin functions 
        theta = np.linspace(np.pi/2, 5*np.pi/2, size)

        #generating x and y values using the random values and theta values 
        x = r*np.cos(theta)
        y = r*np.sin(theta)

        x = np.append(x,x[0])
        y = np.append(y,y[0])

        #gaussian filter is used to reduce noise and smoothen the data 
        x = gaussian_filter(x, sigma=sigma)
        y = gaussian_filter(y, sigma=sigma)
        x[size] = x[0]
        y[size] = y[0]

        imsize=1000
        v = 50
        # rescale image to range [0,100]
        x += v
        y += v
        #fill area inside the curve
        plt.fill_between(x,y)
        plt.axis('off')
        #save plot to buffer
        buf = io.BytesIO()
        plt.savefig(buf)
        buf.seek(0)
        #save buffer to Image
        img = Image.open(buf)
        img = img.convert('L').resize((imsize,imsize))
        #convert Image to array
        arr = np.array(img)
        plt.close()
        #convert image array to 0-1 image
        arr_01 = (arr/255).astype(int)
        # plt.imshow(arr_01)

        return arr_01

    def parasite_data(self,arr_01):
        """ data structure to store microorganism images 
        parameters 
            arr_01 -  microorganism image represented using 0s and 1s 
        returns 
            dictionary where the key is the row number and the values are 
            the start and end index 
        """
        store={}
        n = len(arr_01[0])     
        x = 0

        #storing the first and last occurence of 0s
        for j in range(len(arr_01)): 
            first = -1
            last = -1

            for i in range(0, n):
                if (x != arr_01[j][i]):
                    continue
                if (first == -1):
                    first = i
                last = i

                if (first != -1) :
                    first_last=[first, last]    
                    if first_last==None:
                        continue
                    else:
                        store.update({i: first_last })
        return store 

    def dye_image(self):
        """ function to simulate dye image 
        returns 
            the simulated dye image 
        """
        #initializing a 1000*1000 matrix 
        dye=np.ones([1000,1000],dtype=int)
        #filling the diagonal with 0s
        np.fill_diagonal(dye, 0)
        #filling several strips randomly with 0s
        dye[:,400:450]=0
        dye[800:850,:]=0
        dye[:,600:625]=0
        dyeimage=dye

        #visualizing the dye image 
        # plt.imshow(dyeimage, interpolation='nearest')
        # plt.show()

        return dye 

    def cancer(self,dye, store):
        """function to check if the parasite has cancer or not 
        parameters 
            dye - array used to store dye image 
            store - dict used to store parasite image 
        returns 
            boolean value true corresponds to cancer and false 
            is if the parasite does not have cancer 
        """
        start = time.time()

        #initial matrix to reconstruct the parasite image 
        reconstructed_image=np.ones([1000,1000],dtype=int)
        #storing the row values from the dict 
        rows= store.keys()
        #using dict values to add 0s between start and end index     
        for i in rows:
            reconstructed_image[i][store[i][0]:store[i][1]]=0

        #visualizing the reconstructed image 
        # plt.imshow(reconstructed_image, interpolation='nearest')
        # plt.show()

        #calculating the number of bits of dye inside the parasite 
        dye_=0
        for i in range(len(dye)):
            for j in range(len(dye[0])):
                #checking if the bit in both the images are the same and if it lies inside the parasite 
                if dye[i][j]== reconstructed_image[i][j] and dye[i][j]== 0:
                    dye_ +=1

        #calculating the number of bits of parasite in the microscope image 
        parasite=0
        for i in range(len(reconstructed_image)):
            for j in range(len(reconstructed_image[0])):
                if reconstructed_image[i][j]== 0:
                    parasite +=1

        #calculating the area of dye inside the parasite 
        if (dye_/parasite)*100 >10:
            end = time.time()
            print(format(end-start))
            print("Has cancer") 
        else:
            end = time.time()
            print("Time taken to run cancer detection",format(end-start))
            print("Does not have cancer")
        
    def cancer_optimised(self,dye, store):
        """optimised function to check if the parasite has cancer or not 
        parameters 
            dye - array used to store dye image 
            store - dict used to store parasite image 
        returns 
            boolean value true corresponds to cancer and false 
            is if the parasite does not have cancer 
        """
    
        start = time.time()
        #calculating the number of bits of parasite in the microscope image 
        parasite=0
        val=[]
        for i in range(len(store)):
            x=list(store.values())[0][1]-list(store.values())[0][0]
            parasite +=x

        #calculating the number of bits of dye inside the parasite 
        dye_=0
        for i in store:
            for j in range(len(dye[0])):
                if dye[i][j]== 0 and j>=store[i][0] and j<=store[i][1]:
                    dye_ +=1

        if (dye_/parasite)*100 >10:
            end = time.time()
            print(format(end-start))
            print("Has cancer") 
        else:
            end = time.time()
            print("Time taken to run optimised cancer detection",format(end-start))
            print("Does not have cancer")

def main():
    df=DragonFruit()
    arr_01=df.make_blob()
    store=df.parasite_data(arr_01)
    dye=df.dye_image()
    df.cancer(dye, store)
    df.cancer_optimised(dye, store)
    
    
if __name__=="__main__":
  main()
