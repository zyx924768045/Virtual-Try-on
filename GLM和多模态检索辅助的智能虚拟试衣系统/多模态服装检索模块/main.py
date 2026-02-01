import argparse
import os
import cv2
from functools import reduce
import  numpy as np
from src.data_utils import read_directory, store_db, clear_db, image_db
import src.faiss_clip as faiss_clip
import  src.mysql_operating
import  src.config

# parse args
def get_opt_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--task',
                        type=str,
                        required=True,
                        help='project data name')

    parser.add_argument('--load',
                        action='store_true',
                        help='load data into db')

    parser.add_argument('--index',
                        action='store_true',
                        help='load data text vector into faiss')

    parser.add_argument('--n_total',
                        type=int,
                        default=100,
                        help='take data n_sample,generate it into faiss')

    parser.add_argument('--search',
                        action='store_true',
                        help='search matched image from faiss')

    parser.add_argument('--sentence',
                        type=str,
                        default='',
                        help='query text data')

    parser.add_argument('--topK',
                        type=int,
                        default=5,
                        help='take matched data in topK')

    return parser
def import_db(image_data_list):
    # del
    clear_db()
    # insert
    store_db(image_data_list)
def main(args):
    print('args = ', args)
    task = args.task
    # 1. load data
    if args.load or args.index:
        directory_name='image_data'

        # load_data ,call it method
        id_data, image_data = src.data_utils.read_directory(directory_name)

        image_data_list = list(zip(id_data, image_data))  # -> mysql


    # 2. data storage < id,image>

    if args.load:
        print('*' * 60)
        print("import data into db")
        import_db(image_data_list)
        print('import db success')
    # 3. feature extract(clip)-> faiss

    if args.index:
        # image -> bert( image vector )-> faiss
        print("*" * 60)
        ## conn clip-serving -> image vector

        if args.n_total == -1:
            faiss_clip.add_in_faiss(task, image_data_list)
        else:
            faiss_clip.add_in_faiss(task,  image_data_list[:args.n_total])
        ## image vector -> faiss



    # 4. text search (topK = 4)
    if args.search:
        print("*" * 60)
        query = args.sentence
        print("1.query = ", query)
        if len(query) == 0:
            return

        index = faiss_clip.read_index_in_faiss(task)
        dis, ind = faiss_clip.search_in_faiss( index, query, args.topK)
        print('dis = ', dis)
        print('ind = ', ind)

        print('3. get rank list:')
        # ids-> return datalist( mysql/xxxx )
        ids = ",".join([str(_id) for _id in ind[0]])
        out_put = import_db(ids)
        for i, data in enumerate(zip(dis[0], ind[0])):
            _dis, _ind = data
            _dis = '%.5f' % dis[0][i]
            info = out_put.get(_ind, '')
            print("[No.{}  <{}_{}>]".format(i, _ind, _dis), info)




if __name__ == "__main__":
    args = get_opt_parser().parse_args()
    main(args)