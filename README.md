# Brezenham-VS-SimpleLine-comparison
Implemented both Brezenham and simple line algorithms for drawing lines with time comparison
The test were run with 10 random and 10 000 random lines

![image](https://user-images.githubusercontent.com/48525701/208897971-8a3cc630-3cb8-449d-8470-b54ea100ccbb.png)

![image](https://user-images.githubusercontent.com/48525701/208898016-299e25c3-24b3-4905-bb90-0483af29f121.png)

As we can see from the result Brezenham(mid_point) algorithm is significantly faster than the simple_line

For assurance the test were run backwards with simple line method beeing fisrt this time
![image](https://user-images.githubusercontent.com/48525701/208898177-60c8d8b7-46a4-4611-a7e7-5dda275e31be.png)

![image](https://user-images.githubusercontent.com/48525701/208898232-1645a674-e089-43f8-ad4f-5f7391b3a453.png)

With the results beeing from the same nature we can safely assume that the Brezenham algorithm is faster than the simple line

In the file there are 2 test with preset lines so we can overlook and performance test 

Midpoint:
![image](https://user-images.githubusercontent.com/48525701/208899187-309521db-a10f-4daf-bb17-ff5b0a7bf9a4.png)

SimpleLine:
![image](https://user-images.githubusercontent.com/48525701/208899415-442c2958-ccfa-4cf4-ab8a-fdc1933b6693.png)

For test with this scale both algorithms perform equaly good

For bigger scale we can only assume their equal performance
