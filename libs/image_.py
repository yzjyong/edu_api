import string,random
from PIL import Image,ImageFont,ImageDraw,ImageFilter


def img_code():
    # 生成随机四位数随机验证码
    chars = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(4)])

    # 随机颜色1:
    def rndColor():
        return tuple(random.randint(64, 255) for i in range(3))

    # 随机颜色2:
    def rndColor2():
        return tuple(random.randint(32, 127) for i in range(3))

    # 240 x 60:
    width,height = 60*4,60
    image = Image.new('RGB', (width, height), 'white')
    # 创建Font对象:
    font = ImageFont.truetype('arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), text=chars[t], font=font, fill=rndColor2())
    # 划几根干扰线
    for n in range(2):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='white', width=1)
    image = image.filter(ImageFilter.BLUR)
    image.save('code.png', 'png')
    return image,chars

# @blue.route('/imgcode/')
# def send_img():
#     # 获取图片验证码的UUID即code_id
#     image_code_id = request.args.get("code_id")
#
#     if not image_code_id:
#         abort(403)
#
#     # 生成图片验证码，返回值为图片，文本
#     code_img,chars = img_code()
#     # 将图片验证码保存到redis数据库中
#     try:
#         r.setex(image_code_id,60,chars)
#     except Exception as e:
#         api_logger.error(e)
#     response = make_response(code_img)
#
#     # 设置请求头属性-Content-Type响应的格式
#     response.headers["Content-Type"] = "image/png"
#
#     return response