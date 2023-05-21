'''
Image Embedding
Sydney Arnold
March 2023
'''

''' Standard Library '''
import random
import sys

''' 3rd Party Library '''
from PIL import Image               # pip install pillow
from prettytable import PrettyTable
from collections import OrderedDict

# Pixel tuple index
RED   = 0
GREEN = 1
BLUE  = 2

codeBook = OrderedDict()

codeBook[0] = '0-Dead Drop @: 000'
codeBook[1] = '1-Corner of Lexington Ave and E 48th Street: 001'
codeBook[2] = '2-Corner of Madison Ave and E 34th Street: 010'
codeBook[3] = '3-Drop Package in Potted Plant outside Wells Fargo: 011'
codeBook[4] = '4-Drop Package in Gold Gargage Can: 100'
codeBook[5] = '5-12 PM Sharp: 101'
codeBook[6] = '6-7 AM Sharp: 110'
codeBook[7] = '7-Abort if you see a Red Rose: 111'

usedPixels = []

ogTbl  = PrettyTable(['Pixel', 'R', 'G', 'B',  'COL & ROW'])
altTbl = PrettyTable(['Pixel', 'R', 'G', 'B',  'COL & ROW'])

''' Obtain the Basic image information '''

'''
Image Orientation

         |
         |
y (rows) |
         |
         |     
         -----------------------------
                     x (columns)
'''

print("Embedding in Images Script\n")

try:
    img = Image.open('monalisa.bmp')   
    
    pix = img.load()  
  
    x = 1
    cnt = 1
    
    while x < 6:        
             
        # Pixel to Modify
        r = random.randint(0, img.height-1)  # Row
        c = random.randint(0, img.width-1)   # Col                       
        # Read the Pixel
        pixel = pix[c, r]  
        if (pixel[0] & 1) == 1:  # if red channel has LSB of 1                  
        
            redPx = pixel[RED]      # Extract the RGB
            grnPx = pixel[GREEN]
            bluPx = pixel[BLUE]
            
            binRedPx = '{0:b}'.format(redPx)
            binGrnPx = '{0:b}'.format(grnPx)
            binBluPx = '{0:b}'.format(bluPx)
                          
            ogTbl.add_row([cnt, binRedPx, binGrnPx, binBluPx, [c,r]])
            
            # Print the Current Value of the Pixel
            ogTbl.align = 'l'
            ogTbl.title = "Original Pixels"
            print(ogTbl.get_string(),'\n')        
            
            
            print("Message List:")              # display code book
            for key, value in codeBook.items():
                print('['+str(key)+'] ', value)
                
            print("\nInput the bits corresponding to your message one at a time ({}/5):".format(x)) # get user input
            
            hide = []
            
            for i in range(0, 3):    # get RGB values from user
                bits = int(input())
                hide.append(bits)
            
            if hide[0] == 0:
                redPx = redPx & 0b11111110
            else:
                redPx = redPx | 0b00000001   
                
            if hide[1] == 0:
                grnPx = grnPx & 0b11111110
            else:
                grnPx = grnPx | 0b00000001       
                
            if hide[2] == 0:
                bluPx = bluPx & 0b11111110
            else:
                bluPx = bluPx | 0b00000001    
                
            binRedPx = '{0:b}'.format(redPx)
            binGrnPx = '{0:b}'.format(grnPx)
            binBluPx = '{0:b}'.format(bluPx)            
            
            altTbl.add_row([cnt, binRedPx, binGrnPx, binBluPx, [c,r]])
            
            # Print the Current Value of the Pixel
            altTbl.align = 'l'
            altTbl.title = "Modified Pixels"
            print(altTbl.get_string(),'\n')
            
            # Update the pixel
            pixel = (redPx, grnPx, bluPx)
            
            # Save the changed Pixel in the pixel proper
            pix[c,r] = pixel
            
            # Save this as a new image
            img.save('monaLisaTest.bmp')
            
            x   += 1
            cnt += 1
            
            if x < 6:
                print("\n=============Now Selecting Message {}/5=============\n".format(x)) 
            else:                                           
                print("\nSingle Pixel Steganography Done")
                print("Steganography Results:")
                print(ogTbl.get_string(),'\n')
                print(altTbl.get_string(),'\n')
         
except Exception as err:
    print("Steg Failed: ", str(err))