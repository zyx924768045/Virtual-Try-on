from annoy import AnnoyIndex
import torch
import numpy as np
from model_train.models import ImgModule
from tqdm import tqdm
from config import opt
# 产生image_code
def generate_image_code(img_model, X, bit):
    batch_size = opt.batch_size
    num_data = X.shape[0]
    index = np.linspace(0, num_data - 1, num_data).astype(int)
    B = torch.zeros(num_data, bit, dtype=torch.float)
    if opt.use_gpu:
        B = B.cuda()
    for i in tqdm(range(num_data // batch_size + 1)):
        ind = index[i * batch_size: min((i + 1) * batch_size, num_data)]
        image = X[ind].type(torch.float)
        if opt.use_gpu:
            image = image.cuda()
        cur_f = img_model(image)
        B[ind, :] = cur_f.data

    B = torch.sign(B)
    return B

img_model = ImgModule(opt.bit)
img_model.load('checkpoints/image_model.pth')

if opt.use_gpu:
    img_model = img_model.cuda()
im = np.load(r'D:\pythonProject8\image_data')[100:101]
im = torch.from_numpy(im)
imBX = generate_image_code(img_model, im, opt.bit)
print(imBX.shape)

u = AnnoyIndex(opt.bit, 'hamming')
u.load('test.ann') # super fast, will just mmap the file
print(u.get_nns_by_vector(imBX[0], 3)) # will find the 1000 nearest neighbors





