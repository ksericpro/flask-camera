

# Python3 code to demonstrate 
# to truncate list 
# using del + list slicing
 
# initializing list  
test_list = [1, 4, 5, 6, 7, 3, 8, 9, 10]
 
# printing original list
print ("The original list is : " + str(test_list))
 
# size desired
k = 5
 
# using del + list slicing
# to truncate list 
del test_list[:5]
 
# printing result
print ("The truncated list is : " +  str(test_list))