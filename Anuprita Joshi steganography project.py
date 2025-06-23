import cv2
import matplotlib.pyplot as plt
import numpy as np
import string
import os
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import hashlib

def derive_key(key_str):
    return hashlib.sha256(key_str.encode()).digest()[:16]

def encrypt_message(msg,key_str):
    key=derive_key(key_str)
    cipher=AES.new(key,AES.MODE_CBC)
    ct=cipher.encrypt(pad(msg.encode(),AES.block_size))
    return cipher.iv+ct

def decrypt_message(cipher_bytes,key_str):
    key=derive_key(key_str)
    iv=cipher_bytes[:16]
    ct=cipher_bytes[16:]
    cipher=AES.new(key,AES.MODE_CBC,iv)
    return unpad(cipher.decrypt(ct),AES.block_size).decode()

d={}
c={}
for i in range(256):
    d[chr(i)]=i
    c[i]=chr(i)

print("------ENCRYPTION------")
image_path=input("Enter complete image path:").strip('"')
image_path = os.path.normpath(image_path)
x=cv2.imread(image_path)
xrgb=cv2.cvtColor(x,cv2.COLOR_BGR2RGB)
plt.imshow(xrgb)
plt.title("uploaded image")
plt.axis('off')
plt.show()

key=input("enter key:")
text=input("enter message:")

print("Encrypting text using AES...")
sleep(2)
encrypted_bytes=encrypt_message(text,key)
l=len(encrypted_bytes)
print("Embedding text in image using LSB...")
sleep(2)

n,m,z=0,0,0
kl=0
for i in range(l):
    char_val=d[c[encrypted_bytes[i]]]^d[key[kl]]
    for bit_pos in range(8):
         bit=(char_val>>(7-bit_pos))&1
         org_val=x[n,m,z]
         x[n,m,z]=(org_val & 0xFE)|bit
         #print(f"Embedding bit {bit} at ({n},{m},{z}): {org_val} -> {x[n,m,z]}")
         z=(z+1)%3
         if z==0:
             m=m+1
             if m==x.shape[1]:
                 m=0
                 n=n+1
    kl=(kl+1)%len(key)
cv2.imwrite("encrypting.jpg",x)
plt.imshow(cv2.cvtColor(x,cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("encrypted image")
plt.show()


print("------DECRYPTION------")
n,m,z=0,0,0
kl=0
key1=input("Re-enter key:")
if key==key1:
    print("Decrypting text from image...")
    sleep(2)
    encrypted_back=bytearray()
    for i in range(l):
       val=0
       for bit_pos in range(8):
         bit=x[n,m,z]&1
         val=(val<<1)|bit
         z=(z+1)%3
         if z==0:
             m=m+1
             if m==x.shape[1]:
                 m=0
                 n=n+1
       encrypted_back.append(val^d[key[kl]])
       kl=(kl+1)%len(key)
    decrypted=decrypt_message(bytes(encrypted_back),key)
    print("Decrypted Message:",decrypted)
else:
    print("key mismatch")

