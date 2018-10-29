from django.test import TestCase

# Create your tests here.

for i in range(1,10):
    for j in range(1,10):
        for k in range(1,10):
            z = 6 * i + 8 * j + 9 * k
            if z == 60:
                print(i,j,k)
                exit()