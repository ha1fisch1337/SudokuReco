import cv2
import numpy as np


img = cv2.imread("test_r.jpg")
fimg = cv2.bilateralFilter(img,9,75,75)

edges = cv2.Canny(fimg, 25,250,apertureSize=3)
lines = cv2.HoughLines(edges,1,np.pi/180,201)

width,length=img.shape[0:2]

xm,ym=0,0
xmin,ymin=99999,99999
xcm,ycm=0,0
xcmin,ycmin=0,0




for i in range(len(lines[:,0,0])):
	for rho,theta in lines[i]:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		if theta>2.9:#vert
			x = rho/np.cos(theta)
			if x>xm:
				xm=x
				xcm=((x1,y1),(x2,y2))
				
			if x<xmin:
				xmin=x
				xcmin=((x1,y1),(x2,y2))
				
			
		if 1<theta<1.9:#hor
			y = rho/np.sin(theta)
			if y>ym:
				ym=y
				ycm=((x1,y1),(x2,y2))
				
			if y<ymin:
				ymin=y
				ycmin=((x1,y1),(x2,y2))
			

# cv2.line(img,xcm[0],xcm[1],(255,0,255),5)#right
# cv2.line(img,xcmin[0],xcmin[1],(255,0,255),5)#left
# cv2.line(img,ycm[0],ycm[1],(255,0,255),5)#low
# cv2.line(img,ycmin[0],ycmin[1],(255,0,255),5)#high

def le(x1,y1,x2,y2):#line equation
	#y1=kx1+b
	#y2=kx2+b
	k=(y1-y2)/(x1-x2)
	b=y1-k*x1
	return k,b
	
def lec(k1,b1,k2,b2):#line equations cross
	x=(b2-b1)/(k1-k2)
	return x

def ybyx(x,k,b):#y by x
	return k*x+b

k1,b1=(le(xcm[0][0],xcm[0][1],xcm[1][0],xcm[1][1]))#right
k2,b2=(le(xcmin[0][0],xcmin[0][1],xcmin[1][0],xcmin[1][1]))#left
k3,b3=(le(ycm[0][0],ycm[0][1],ycm[1][0],ycm[1][1]))#low
k4,b4=(le(ycmin[0][0],ycmin[0][1],ycmin[1][0],ycmin[1][1]))#high

x_0=lec(k2,b2,k4,b4)
x_right=lec(k1,b1,k4,b4)
x_low=lec(k2,b2,k3,b3)
x_y=lec(k1,b1,k3,b3)

y_0=ybyx(x_0,k2,b2)
y_right=ybyx(x_right,k1,b1)
y_low=ybyx(x_low,k2,b2)
y_x=ybyx(x_y,k1,b1)

pts1=np.float32([[x_0,y_0],[x_right,y_right],[x_low,y_low],[x_y,y_x]])
pts2=np.float32([[width*.1,length*.1],[width*.9,length*.1],[width*.1,length*.9],[width*.9,length*.9]])

print(pts1,pts2,sep='\n')

matrix=cv2.getPerspectiveTransform(pts1,pts2)
result=cv2.warpPerspective(img,matrix,(width,length))

cv2.imwrite('out_r.jpg',result)
