from PIL import Image, ImageOps
import easyocr

m=[]
def catch(filename):
    image=Image.open(filename)
    h,w=image.size
    reader=easyocr.Reader(['en'],verbose=False,gpu=False)
    for i in range(9):
        a=[]
        for j in range(9):
            cropped_image=image.crop((j*h//9,i*w//9,(j+1)*h//9,(i+1)*w//9))
            cropped_image.save("stock/a.jpg")
            try:
                a.append(reader.readtext("stock/a.jpg",detail=0))
            except:
                a.append(' ')
        m.append(a)
    print(*m,sep='\n')

def make_image():
    pass