#!/usr/bin/python3.2

def main():
  #the books hello world
  msg = [7,4,11,11,14,26,22,14,17,11,3]
  print (msg)
  #cipher with public key
  x = cipher()
  #decipher with private key
  y = dcipher()
  #cipher with private key
  z = cipher()
  #decipher with public key
  w = dcipher()
  
  wprint(w)
  wprint(y)
  
  #now find big enough p, q, e, and d so this works
  msg = [x+ord('a') for x in msg]
  x = cipher()
  y = dcipher()
  wprint2(y)

def cipher(m,e,n):
  return [pow(x,e,n) for x in m]

def dcipher(c,d,n):
  return cipher(c,d,n)

def wprint(y):
  for c in y:
    if c == 26:
      print(" ",end = "")
    else:
      print("%s"%((chr(c+97))),end = "")
  print ()

def wprint2(y):
  for c in y:
    if chr(c) == '{':
      print(" ",end = "")
    else:
      print(chr(c), end = "")
  print ()

#found this code somewhere
def egcd(a, b):
  x,y, u,v = 0,1, 1,0
  while a != 0:
    q,r = b//a,b%a; m,n = x-u*q,y-v*q
    b,a, x,y, u,v = a,r, u,v, m,n
  return b, x, y

#function to find d in RSA
#must give e and totient
#stole this code too :)
def modinv(a, m):
  g, x, y = egcd(a, m)
  if g != 1:
    return None  # modular inverse does not exist
  else:
    return x % m

if __name__ == "__main__":
  main()
