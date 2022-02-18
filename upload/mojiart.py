from PIL import Image, ImageFont, ImageDraw
import numpy as np
import  random

def resize_strimg(IMG):
    global GIF, ONES, SMAX, SMIN, FONT, ORGIMG, MSKIMG, DIR, BACKGROUND, SPACE, str_img, c, org_img, w, h, org_img_array, msk_img, msk_img_array, img, img2, tmp_img, img_array, img2_array, tmp_img_array, gif_img, strings
    img_array = np.array(IMG)
    index = np.where(np.all(img_array[:, :] == [0, 0, 0, 255], axis=2))
    img = Image.fromarray(img_array).crop((min(index[1])-SPACE, min(index[0])-SPACE, max(index[1])+SPACE, max(index[0])+SPACE))
    return img

def init(orgimg, mskimg):
    global GIF, ONES, SMAX, SMIN, FONT, ORGIMG, MSKIMG, DIR, BACKGROUND, SPACE, str_img, c, org_img, w, h, org_img_array, msk_img, msk_img_array, img, img2, tmp_img, img_array, img2_array, tmp_img_array, gif_img, strings

    GIF = False #GIFの生成をするか(Google colabだとオフにしたほうがいいかも？)
    ONES = True #1文字の配置率を低くするか

    #設定
    strings = ("mario", "マ\nリ\nオ", "スーパーマリオ", "任天堂", "ルイ\nージ", "ピーチ", "ク\nッ\nパ", "まりお", "ブラザーズ", "Super Mario", "MARIO", "M\na\nr\ni\no", "M", "クリ\nボー", "きのこ", "L") #\nで文字を縦に
    SMAX = 25 #最大ピクセル
    SMIN = 15 #最小ピクセル
    FONT = 'meiryo.ttc'

    ORGIMG = orgimg
    MSKIMG = mskimg
    DIR = "./"

    BACKGROUND = (128, 128, 128, 255)

    #Google colab用
    '''
    DIR = "/content/drive/MyDrive/mojiart/"
    FONT = DIR+'meiryo.ttc'
    ORGIMG = DIR+"mario.png"
    MSKIMG = DIR+"mario00.png"
    '''

    #文字画像の生成
    SPACE = 15

    str_img = []
    font = ImageFont.truetype(FONT, 100)
    for i in range(len(strings)):
        c = strings[i].count("\n")
        fw, fh = font.getsize(strings[i])
        moji_img = Image.new("RGBA", (max(fw, fh)*2, max(fw, fh)*2), (0, 0, 0, 0)) #文字の生成
        draw = ImageDraw.Draw(moji_img)
        draw.text((int(fw*0.2), int(fh*0.2)), strings[i], font=font, fill=(0, 0, 0, 255))

        moji_img = resize_strimg(moji_img)
        str_img.append(moji_img)


    #元画像　マスク画像　入力
    org_img = Image.open(ORGIMG).convert("RGB")
    w, h = org_img.size
    org_img_array = np.array(org_img.convert("RGBA"))
    msk_img = Image.open(MSKIMG).convert("RGB").resize((w, h))
    msk_img_array = np.array(msk_img)


    #生成画像　TEMP画像　作成
    img = Image.new("RGBA", (w, h), BACKGROUND)
    img2 = Image.new("RGBA", (w, h), BACKGROUND)
    tmp_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img_array = np.array(img)
    img2_array = np.array(img2)
    tmp_img_array = np.array(tmp_img)


    gif_img = []

def setstr(str_img, i_a, i2_a, t_i_a, w, h, x, y, msk_img_array, I):
    global GIF, ONES, SMAX, SMIN, FONT, ORGIMG, MSKIMG, DIR, BACKGROUND, SPACE, c, org_img, org_img_array, msk_img, img, img2, tmp_img, img_array, img2_array, tmp_img_array, gif_img, strings
    N = 0
    img_array = i_a
    img2_array = i2_a
    tmp_img_array = t_i_a
    ssize = random.randint(SMIN, max(SMAX-I, SMIN+1))
    rand = random.randint(0, len(str_img)-1)
    moji_img = str_img[rand]
    mw, mh = moji_img.size
    if mw*2 >= mh:
        if ONES == True and len(strings[rand]) == 1 and random.randint(0, 4) >= 1:
            return (img_array, img2_array, tmp_img_array, N)
        mw, mh = (int(mw * ssize/mh), ssize)
    else:
        if random.randint(0, 10) >= 1:
            return (img_array, img2_array, tmp_img_array, N)
        mw, mh = (ssize, int(mh * ssize/mw))


    if x+mw >= w or y+mh >= h:
        return (img_array, img2_array, tmp_img_array, N)
    
    cant_set = False
    B = 3
    for i in range(B):
        w1 = (mw//B)
        w2 = 0
        i2 = i+1
        if i == B-1:
            w2 = mw%B

        if np.all(np.all(tmp_img_array[y:y+mh, x+w1*i:x+w1*i2+w2] == [0, 0, 0, 0], axis=2)) == True and \
            np.all(np.all(msk_img_array[y:y+mh, x+w1*i:x+w1*i2+w2] == [0, 0, 0], axis=2)) == True:
            continue
        else:
            cant_set = True
            return (img_array, img2_array, tmp_img_array, N)
    
    if cant_set == False:
        moji_img = moji_img.resize((mw, mh))
        moji_img_array = np.array(moji_img)
        index = np.where(moji_img_array[:, :, 3] != 0)
        tmp_img_array[y:y+mh, x:x+mw] = [255, 0, 0, 255]
        img_array[y+index[0], x+index[1]] = [0, 0, 0, 255]
        img2_array[y+index[0], x+index[1]] = org_img_array[y+(mh//2), x+(mw//2)]
        N = 1
        if GIF == True:
            gif_img.append(Image.fromarray(img2_array).convert("RGB"))

    return (img_array, img2_array, tmp_img_array, N)


def main(orgimg, mskimg):
    global GIF, ONES, SMAX, SMIN, FONT, ORGIMG, MSKIMG, DIR, BACKGROUND, SPACE, str_img, c, org_img, w, h, org_img_array, msk_img, msk_img_array, img, img2, tmp_img, img_array, img2_array, tmp_img_array, gif_img
    init(orgimg, mskimg)
    N = -1
    I = 1
    while(N != 0):
        if N != -1:
            N = 0
            msk_index = np.all(msk_img_array[:, :] == [0, 0, 0], axis=2)
            tmp_index = np.all(tmp_img_array[:, :] == [0, 0, 0, 0], axis=2)
            index = np.where(msk_index&tmp_index)

            for i in range(len(index[0])):
                (img_array, img2_array, tmp_img_array, x) = setstr(str_img, img_array, img2_array, tmp_img_array, w, h, index[1][i], index[0][i], msk_img_array, I)
                N += x
        else:
            index = np.where(np.all(msk_img_array[:, :] == [0, 0, 0], axis=2))
            lurd = (min(index[1]), min(index[0]), max(index[1]), max(index[0]))
            for y in range(lurd[1], lurd[3]+1):
                for x in range(lurd[0], lurd[2]+1-SMIN):
                    if np.all(msk_img_array[y, x] == [0, 0, 0]) == True and np.all(tmp_img_array[y, x] == [255, 0, 0, 255]) == False:
                        (img_array, img2_array, tmp_img_array, x) = setstr(str_img, img_array, img2_array, tmp_img_array, w, h, x, y, msk_img_array, I)
                        N += x
        print(N)
        I += 1

    #img = Image.fromarray(img_array)
    #img.save(DIR+"mono.png")

    #index = np.where(np.all(img_array[:, :] == [0, 0, 0, 255], axis=2))
    #img2_array[index] = org_img_array[index]
    img2 = Image.fromarray(img2_array)
    #img2.save(DIR+"color.png")

    if GIF == True:
        gif_img[0].save(DIR+"a.gif", save_all=True, append_images=gif_img[1:], optimize=False, duration=30, loop=0)
    return img2
