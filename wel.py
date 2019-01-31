'''
TCP Server Version 1.0
2019/1/28
zhongming
    此类用于生成欢迎词图片
'''
from PIL import Image, ImageDraw, ImageFont


def draw_image(new_img, text, text2, text3, show_image=False):
    text = str(text)
    text2 = str(text2)
    text3 = str(text3)
    draw = ImageDraw.Draw(new_img)
    img_size = new_img.size
    font_size = 100

    fnt = ImageFont.truetype('simsun.ttc', font_size, encoding="utf-8")
    fnt_size = fnt.getsize(text)
    while fnt_size[0] > img_size[0] or fnt_size[0] > img_size[0]:
        font_size -= 5
        fnt = ImageFont.truetype('simsun.ttc', font_size, encoding="utf-8")
        fnt_size = fnt.getsize(text)

    fnt2 = ImageFont.truetype('simsun.ttc', font_size, encoding="utf-8")
    fnt_size2 = fnt2.getsize(text2)
    while fnt_size2[0] > img_size[0] or fnt_size2[0] > img_size[0]:
        font_size -= 5
        fnt2 = ImageFont.truetype('simsun.ttc', font_size, encoding="utf-8")
        fnt_size2 = fnt2.getsize(text2)

    fnt3 = ImageFont.truetype('simsun.ttc', font_size, encoding="utf-8")
    fnt_size3 = fnt3.getsize(text3)
    while fnt_size3[0] > img_size[0] or fnt_size3[0] > img_size[0]:
        font_size -= 5
        fnt3 = ImageFont.truetype('simsun.ttc', font_size, encoding="utf-8")
        fnt_size3 = fnt3.getsize(text3)

    x = (img_size[0] - fnt_size[0]) / 2
    y = (img_size[1] - fnt_size[1]) / 4

    x2 = (img_size[0] - fnt_size2[0]) / 2
    y2 = (img_size[1] - fnt_size2[1]) / 2

    x3 = (img_size[0] - fnt_size3[0]) / 2
    y3 = (img_size[1] - fnt_size3[1]) / 1.3

    print("x", x, y)
    print("x2", x2, y2)
    print("x3", x3, y3)

    draw.text((x, y), text, font=fnt, fill=(255, 255, 0))
    draw.text((x2, y2), text2, font=fnt, fill=(255, 255, 0))
    draw.text((x3, y3), text3, font=fnt, fill=(255, 255, 0))

    if show_image:
        new_img.show()
    del draw


def new_image(width, height, text='default', text2='热烈欢迎', text3='莅临我司指导工作', color=(255, 0, 0, 255),
              show_image=False):
    new_img = Image.new('RGBA', (int(width), int(height)), color)
    draw_image(new_img, text, text2, text3, show_image)
    new_img.save(r'D:\\src\\wel\\wel.png')
    del new_img


def new_image_with_file(fn):
    with open(fn, encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if l:
                ls = l.split(',')
                if '#' == l[0] or len(ls) < 2:
                    continue
                new_image(*ls)

# if '__main__' == __name__:
# new_image(1600, 900, '三棱科技智慧物联发展股份有限公司领导', '热烈欢迎', '莅临我司指导工作', show_image=True)
