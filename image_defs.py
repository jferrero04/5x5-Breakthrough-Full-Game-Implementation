#!/usr/bin/env python
# coding: utf-8

# In[1]:


def straighten_image(image,corners=None):
    import numpy as np
    import cv2

    
    if corners is None:
        corners=find_corners(image)

    top_left, top_right, bottom_right, bottom_left=corners
    # Define the width and height of the new "top-down" view
    width = int(max(
        np.linalg.norm(bottom_right - bottom_left),
        np.linalg.norm(top_right - top_left)
    ))
    height = int(max(
        np.linalg.norm(top_right - bottom_right),
        np.linalg.norm(top_left - bottom_left)
    ))

    # Define the destination points for the perspective transform
    destination_corners = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(corners, destination_corners)
    
    # Apply the perspective transformation
    warped_image = cv2.warpPerspective(image, matrix, (width, height))

    return warped_image


# In[2]:


def get_board_squares_from_image(image,board_size,square_size=(60,60)):
    import numpy as np
    import cv2
    nr,nc=board_size
    
    squares=[]
    pix_row=image.shape[0]//nr
    pix_col=image.shape[1]//nc
    
    count=1
    for r in range(nr):
        for c in range(nc):
            subim=image[ pix_row*r:pix_row*(r+1),
                        pix_col*c:pix_col*(c+1),
                        :]
            subim=cv2.resize(subim,square_size)

            squares.append(subim)

    return squares


# In[4]:


def get_gray_and_threshold_image(image,threshold,fill_sides=True):
    import numpy as np
    import cv2

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = image.shape[:2]
    threshold_im=((gray<threshold)*255).astype(np.uint8)

    if fill_sides:
        # fill in the side parts that are off the grid
        val=0
        cv2.floodFill(threshold_im,None,(0,0),val)
        cv2.floodFill(threshold_im,None,(w-1,0),val)
        cv2.floodFill(threshold_im,None,(w-1,h-1),val)
        cv2.floodFill(threshold_im,None,(0,h-1),val)   


    return gray,threshold_im


# In[ ]:


def find_corners(threshold_image,plotit=False):
    import numpy as np
    from pylab import figure,imshow,plot
    import cv2
    
    idx=np.where(threshold_image>126)
    points=[]
    for (i,j) in zip(idx[0],idx[1]):
        points.append((j,i))
    
    points=np.array(points)
    xp=points[:,0]
    yp=points[:,1]
    
    import scipy.spatial
    hull = scipy.spatial.ConvexHull(points)
    hull_points = points[hull.vertices]

    x=hull_points[:,0]
    y=hull_points[:,1]


    if plotit:
        imshow(threshold_image)
        plot(xp,yp,'.')
        plot(x,y,'o-')

    
    h,w=threshold_image.shape
    corners=[]    
    for x2,y2 in [ [w,h], [0,h],[0,0],[w,0]  ]:
        d=(x-x2)**2+(y-y2)**2
        idx=np.argmax(d)
    
        corners.append([x[idx],y[idx]])
    corners=np.array(corners,dtype=np.float32)
    
    if plotit:
        plot(corners[:,0],corners[:,1],'*')

    return corners

