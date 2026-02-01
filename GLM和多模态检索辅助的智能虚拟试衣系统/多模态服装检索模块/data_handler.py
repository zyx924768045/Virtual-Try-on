import h5py
import scipy.io as scio
import numpy as np

def load_data(images_path,labels_path,tags_path):
    # file = h5py.File(path)
    # print(file)
    # images = file['IAll'][:1000]
    images = np.load(images_path)[:100].astype('float')
    print('images.shape:',images.shape)
    # labels = file['LAll'][:1000]
    labels = np.load(labels_path)[:100].astype('float')
    print('labels.shape',labels.shape)
    # tags = file['YAll'][:1000]
    tags = np.load(tags_path)[:100].astype('float')
    print('tags.shape',tags.shape)

    # file.close()
    return images, tags, labels


def load_pretrain_model(path):
    return scio.loadmat(path)


if __name__ == '__main__':
    tags = np.load(tags_path)[:100].astype('float')
    pass
    # a = {'s': [12, 33, 44],
    #      's': 0.111}
    # import os
    # with open('result.txt', 'w') as f:
    #     for k, v in a.items():
    #         f.write(k, v)
