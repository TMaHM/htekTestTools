from PhoneLib.htek_phone_conf import *
from config.usr_data import *
from PIL import Image

# path = drd_UC924E.screen_shot('test_acd')
# print(path)
# img = Image.open(path)
# print(img.size)
# crop = img.crop((379, 10, 402, 38))
# standard_img_path = '{tmp_path}/drd_uc924e_acd.jpg'.format(tmp_path=IMG_STANDARD_PATH)
# crop.save(standard_img_path)
# r = drd_UC924E.acd(method='in', solution='drd')
# print(r)
# r = drd_UC926.acd(method='in', solution='drd')
# print(r)

#
# def capture(phone, solution, func):
#     path = '{std_path}/{solution}_{model}_{func}.jpg'.format(std_path=IMG_STANDARD_PATH, solution=solution,
#                                                              model=phone.model.lower(),
#                                                              func=func)
#     tmp = phone.screen_shot('test_temp')
#     img = Image.open(tmp)
#     pixel = acd_pixel_dir[func][phone.model.lower()][solution.lower()]
#     cropped = img.crop(pixel)
#     cropped.save(path)
#
#
# # capture(drd_UC924E, 'drd', 'acd_out')
#
# # r = drd_UC924E.acd(method='out', solution='drd')
# r = drd_UC924E.acd(method='in', solution='drd')
# print(r)
