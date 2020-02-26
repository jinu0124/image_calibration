from PIL import Image
import os
import argparse

#C:\Users\jinwo\Anaconda3\envs\lowpython\Lib\site-packages 에서 resize.py 수행하기
#print(os.listdir(directory))
#directory = "C:\\Users\jinwo\magicwand\source\\tan\check"
def rescale_images(directory, size):
    for img in os.listdir(directory):
        im = Image.open(directory + img) #open image from directory
        im_resized = im.resize(size, Image.ANTIALIAS) #image resize to size
        im_resized.save(directory + img) # image save


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale Images")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory')
    parser.add_argument('-s', '--size', type=int, nargs=2, required = True)
    args = parser.parse_args()
    rescale_images(args.directory, args.size)

