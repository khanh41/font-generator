import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# font = ImageFont.truetype("Arial-Bold.ttf",14)
font = ImageFont.truetype("tvN 즐거운이야기 Light.ttf",50)
img=Image.new("RGBA", (500,250),(255,255,255))
draw = ImageDraw.Draw(img)
draw.text((0, 0),"그들의 장비와 기구는 모두 살아 있다.",(0,0,0),font=font)
draw = ImageDraw.Draw(img)
img.save("a_test.png")
