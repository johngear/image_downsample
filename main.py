import PIL
from PIL import Image

import numpy as np

### I AM ONCE AGAIN CODING FOR FUN

### if you are reading this, there's some functions wrote twice because men are born free and can write a better version of a function but keep the old one


def try_encrypt():

    #this stuff was mostly pulled from stack overflow
    try:
        # take path of image as a input
        path = input(r'Enter path of Image : ')
        
        # taking encryption key as input
        key = int(input('Enter Key for encryption of Image : '))
        
        # print path of image file and encryption key that
        # we are using
        print('The path of file : ', path)
        print('Key for encryption : ', key)
        
        # open file for reading purpose
        fin = open(path, 'rb')
        
        # storing image data in variable "image"
        image = fin.read()
        fin.close()
        
        # converting image into byte array to
        # perform encryption easily on numeric data
        image = bytearray(image)

        # performing XOR operation on each value of bytearray
        for index, values in enumerate(image):
            image[index] = values ^ key

        # opening file for writing purpose
        fin = open(str(path[:-4] + "_ENCRYPT.png"), 'wb')
        
        # writing encrypted data in image
        fin.write(image)
        fin.close()
        print('Encryption Done...')

        
    except Exception:
        print('Error caught : ', Exception.__name__)

def encrypt(image_path: str, encryption_key: int):
    fin = open(image_path, 'rb')
    image = fin.read()
    fin.close()

    #idk this seems like a super easy way to "encryp" but you could sub in any advanced method here
    image = bytearray(image)

    for index, values in enumerate(image):
        image[index] = values ^ encryption_key

    fin = open(str(image_path[:-4] + "_encrypt.png"), 'wb')
    fin.write(image)
    fin.close()

    print('Encryption Done...')

def try_decrypt():
    try:
        # take path of image as a input
        path = input(r'Enter path of Image : ')
        
        # taking decryption key as input
        key = int(input('Enter Key for encryption of Image : '))
        
        # print path of image file and decryption key that we are using
        print('The path of file : ', path)
        print('Note : Encryption key and Decryption key must be same.')
        print('Key for Decryption : ', key)
        
        # open file for reading purpose
        fin = open(path, 'rb')
        
        # storing image data in variable "image"
        image = fin.read()
        fin.close()
        
        # converting image into byte array to perform decryption easily on numeric data
        image = bytearray(image)
    
        # performing XOR operation on each value of bytearray
        for index, values in enumerate(image):
            image[index] = values ^ key
    
        # opening file for writing purpose
        fin = open(str(path[:-4] + "OUT.png"), 'wb')
        
        # writing decryption data in image
        fin.write(image)
        fin.close()
        print('Decryption Done...')
    
    
    except Exception:
        print('Error caught : ', Exception.__name__)

def decrypt(image_path: str, encryption_key: int):
    
    fin = open(image_path, 'rb')
        
    image = fin.read()
    fin.close()
    
    # converting image into byte array to perform decryption easily on numeric data
    image = bytearray(image)

    # performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ encryption_key

    # opening file for writing purpose
    fin = open(str(image_path[:-4] + "_decrypt.png"), 'wb')
    
    # writing decryption data in image
    fin.write(image)
    fin.close()
    print('Decryption Done...')




# try_encrypt()
# try_decrypt()


## it works
def view_images():
    
    image = Image.open('test_pic.png')
    image2 = Image.open('test_pic_ENCRYPTOUT.png')
    # summarize some details about the image

    print(image.format)
    print(image.size)
    print(image.mode)
    # show the image
    # image.show()

    data = np.asarray(image)
    data2 = np.asarray(image2)

    ## this shows if there is any pixel level differneces between the two images
    print(sum(sum(abs(data - data2))))


def construct_downsampled_images(input_image_path):
    
    image = Image.open(input_image_path)
    im_array = np.asarray(image)

    im_array2 = np.zeros_like(im_array)
    im_array4 = np.zeros_like(im_array)
    im_array8 = np.zeros_like(im_array)

    x,y,_ = np.shape(im_array) #z is 4, since these are PNGs, this should be 3 or 4 chanel agnostic though

    for iter in [2,4,8]:
        for i in range(0,int(x/iter)):
            for j in range(0,int(y/iter)):

                new_pix = np.average(np.average(im_array[iter*i : iter*i +iter, iter*j : iter*j +iter], axis=0), axis=0) #should be shape (4,)
                assert np.shape(new_pix) == (4,) #would need to change for new image types
                
                if iter==2:
                    # new_pix = np.average(np.average(im_array[2*i : 2*i +iter, 2*j : 2*j +iter], axis=0), axis=0) #should be shape (4,)
                    # assert np.shape(new_pix) == (4,) #would need to change for new image types
                    im_array2[iter*i : iter*i +iter, iter*j : iter*j +iter] = np.stack(((new_pix,new_pix),(new_pix,new_pix)))
                elif iter==4 and np.shape(im_array4[4*i : 4*i + iter, 4*j : 4*j + iter ]) == (4,4,4):
            
                    # new_pix = np.array([256,128,0,256])
                    # area = np.stack(((new_pix,new_pix,new_pix,new_pix),(new_pix,new_pix,new_pix,new_pix),(new_pix,new_pix,new_pix,new_pix),(new_pix,new_pix,new_pix,new_pix)))
                    area = np.zeros((iter,iter,4))

                    for k in range(0,iter):
                        for l in range(0,iter):
                            area[k,l,:] = new_pix
                            # print("entered")

                    im_array4[iter*i : iter*i +iter, 4*j : iter*j +iter ] = area
                    # print("entered")
                elif iter==8 and np.shape(im_array4[iter*i : iter*i + iter, iter*j : iter*j + iter ]) == (8,8,4):

                    area = np.zeros((iter,iter,4))

                    for k in range(0,iter):
                        for l in range(0,iter):
                            area[k,l,:] = new_pix
                            # print("entered")

                    im_array8[iter*i : iter*i +iter, iter*j : iter*j +iter] = area

    new_im_2 = Image.fromarray(im_array2)
    new_im_4 = Image.fromarray(im_array4)
    new_im_8 = Image.fromarray(im_array8)

    image.show()
    new_im_2.show()
    new_im_4.show()
    new_im_8.show()

#Generalized version of the above function, for any downsampling needed   
def construct_downsampled_IMAGE(input_image_path, iter: int):
    
    image = Image.open(input_image_path)
    im_array = np.asarray(image)
    im_array2 = np.zeros_like(im_array)

    x,y,z = np.shape(im_array)

    for i in range(0,int(x/iter)):
        for j in range(0,int(y/iter)):

            new_pix = np.average(np.average(im_array[iter*i : iter*i +iter, iter*j : iter*j +iter], axis=0), axis=0) #should be shape (4,)
            assert np.shape(new_pix) == (z,) #would need to change for new image types
            
            if np.shape(im_array2[iter*i : iter*i + iter, iter*j : iter*j + iter ]) == (iter,iter,4):
        
                area = np.zeros((iter,iter,z))
                for k in range(0,iter):
                    for l in range(0,iter):
                        area[k,l,:] = new_pix
                        
                im_array2[iter*i : iter*i +iter, iter*j : iter*j +iter ] = area
    
    return(Image.fromarray(im_array2))
    # new_im_2.show()




# construct_downsampled_images('test_pic.png')
# construct_downsampled_IMAGE('test_pic.png', 5).show()

if __name__ == "__main__":
    #run program

    image2 = construct_downsampled_IMAGE('test_pic.png', 2)
    image4 = construct_downsampled_IMAGE('test_pic.png', 4)
    # image8 = construct_downsampled_IMAGE('test_pic.png', 8)

    image2_path = 'image2.png'
    image4_path = 'image4.png'

    image2.save(image2_path, "PNG")
    image4.save(image4_path, "PNG")

    key2 = 89
    key4 = 110

    encrypt(image2_path, key2)
    encrypt(image4_path, key4)

    decrypt( str(image2_path[:-4] + "_encrypt.png"), key2)
    decrypt( str(image4_path[:-4] + "_encrypt.png"), key4)


    print("pause")
    print("pause")