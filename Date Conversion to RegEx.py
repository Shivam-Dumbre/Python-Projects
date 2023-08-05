def Greg2JD(year, month, day):

    if (month < 3):
        y = float(year) - 1.0
        m = float(month) + 12.0
    else:
        y = float(year)
        m = float(month)
    a = 0; b = 0
    if (y + m / 12 + float(day) / 365 > 1582.87166):
        a = int(y / 100)
        b = 2 - a + int(float(a / 4))
    c = 0
    if (y < 0.0):
        c = int(365.25 * y - 0.75)
    else:
        c = int(365.25 * y)
    d = int(30.6001 * (m + 1))
    jd = float(b + c + d + day + 1720994.5);

    return jd

    
def QuarterDates(quarter):

    Qstart = [2454953.5,2454964.5,2454998.5]
    Qstop  = [2454962.5,2454997.5,2455100.5]
    if (quarter < len(Qstart)):
        return Qstart[quarter] - 10, Qstop[quarter] + 10
    else:
        message  = 'No spacecraft roll dates recorded for quarter ' + str(quarter) + '.\n'
        message += 'Find an updated script at http://keplergo.arc.nasa.gov'
        sys.exit(message)
        
        def Remove(tuples):
    tuples = [t for t in tuples if t]
    return tuples
 
# Driver Code
tuples = [(), ('ram','15','8'), (), ('laxman', 'sita'),
          ('krishna', 'akbar', '45'), ('',''),()]
print(Remove(tuples))
def Repeat(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(x[i])
    return repeated
 
# Driver Code
list1 = [10, 20, 30, 20, 20, 30, 40,
         50, -20, 60, 60, -20, -20]
print (Repeat(list1))

# initializing lists
test_list = [["Gfg", "good"], ["is", "for"], ["Best"]]
 
# printing original list
print("The original list : " + str(test_list))
 
# using loop for iteration
res = []
N = 0
while N != len(test_list):
    temp = ''
    for idx in test_list:
         
        # checking for valid index / column
        try: temp = temp + idx[N]
        except IndexError: pass
    res.append(temp)
    N = N + 1
 
res = [ele for ele in res if ele]
 
# printing result
print("List after column Concatenation : " + str(res))

# string is palindrome or not
def palindrome(a):
  
    # finding the mid, start
    # and last index of the string
    mid = (len(a)-1)//2     #you can remove the -1 or you add <= sign in line 21 
    start = 0                #so that you can compare the middle elements also.
    last = len(a)-1
    flag = 0
 
    # A loop till the mid of the
    # string
    while(start <= mid):
  
        # comparing letters from right
        # from the letters from left
        if (a[start]== a[last]):
             
            start += 1
            last -= 1
             
        else:
            flag = 1
            break;
             
    # Checking the flag variable to
    # check if the string is palindrome
    # or not
    if flag == 0:
        print("The entered string is palindrome")
    else:
        print("The entered string is not palindrome")
         
# Function to check whether the
# string is symmetrical or not       
def symmetry(a):
     
    n = len(a)
    flag = 0
     
    # Check if the string's length
    # is odd or even
    if n%2:
        mid = n//2 +1
    else:
        mid = n//2
         
    start1 = 0
    start2 = mid
     
    while(start1 < mid and start2 < n):
         
        if (a[start1]== a[start2]):
            start1 = start1 + 1
            start2 = start2 + 1
        else:
            flag = 1
            break
      
    # Checking the flag variable to
    # check if the string is symmetrical
    # or not
    if flag == 0:
        print("The entered string is symmetrical")
    else:
        print("The entered string is not symmetrical")
         
# Driver code
string = 'amaama'
palindrome(string)
symmetry(string)
def checkEmpty(input, pattern):
     
    # If both are empty
    if len(input)== 0 and len(pattern)== 0:
        return 'true'
 
    # If only pattern is empty
    if len(pattern)== 0:
        return 'true'
 
    while (len(input) != 0):
 
        # find sub-string in main string
        index = input.find(pattern)
 
        # check if sub-string founded or not
        if (index ==(-1)):
            return 'false'
 
        # slice input string in two parts and concatenate
        input = input[0:index] + input[index + len(pattern):]           
    return 'true'
 
# Driver program
if __name__ == "__main__":
    input ='GEEGEEKSKS'
    pattern ='GEEKS'
    print (checkEmpty(input, pattern))