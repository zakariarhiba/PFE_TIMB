nums = ['3', ' 5', ' 7', ' 23']
nums = [int(num) for num in nums]

min = 10000
max = 0

for num in nums:
    if (num < min) :
        min = num
    if (num > max) :
        max = num
        
print(f"the max = {max} \nthe min = {min}")