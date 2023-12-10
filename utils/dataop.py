from typing import List,Callable,Tuple
import Augmentor as ag

def augment_dataset(dataset:str,percentage:int=100,file_extension:str="png",
                    writer:Callable[[str],None]=print,
                    seed:int=3211,flip_lr:float = 0.5,flip_tb:float = 0.5,
                    zoom_rand:dict = {"probability":0.4,"percentage_area":0.7},
                    distortion:dict = {"probability":0.0,"grid_width":4,"grid_height":4,"magnitude":8},
                    erasing:dict = {"probability":0.0,"rectangle_area":0.1},
                    crop:dict = {"probability":0.5, "percentage_area":0.7},
                    mixer:dict = {"probability":0.7,"min_factor":0.7,"max_factor":1}
                    ) -> None:
        from os import listdir,mkdir
        from os.path import abspath,join
        dataset = abspath(dataset)
        format_dataset(dataset,extension=file_extension,writer=writer)
        try:
            mkdir(join(dataset,"temp"))
        except:
            pass

        temp_path = abspath(join(dataset,"temp"))
        temp_imgs = listdir(dataset)
        imgs_extension = file_extension
        num_images = int((percentage/100)*len(temp_imgs))
        del temp_imgs

        pipeline = ag.Pipeline(dataset,temp_path,save_format=imgs_extension) 
        pipeline.set_seed(seed=seed)
        
        if not flip_lr == 0:
            pipeline.flip_left_right(flip_lr)
        if not flip_tb == 0:
            pipeline.flip_top_bottom(flip_tb)
        if not zoom_rand["probability"] == 0:
            pipeline.zoom_random(**zoom_rand)
        if not distortion["probability"] == 0:
            pipeline.random_distortion(**distortion)
        if not erasing["probability"] == 0:
            pipeline.random_erasing(**erasing)
        if not crop["probability"] == 0:
            pipeline.crop_centre(**crop)
        if not mixer["probability"] == 0:
            pipeline.random_contrast(**mixer)
            pipeline.random_color(**mixer)
            pipeline.random_brightness(**mixer)

        pipeline.sample(num_images)

        writer("moving and treating dataset processed")
        treating_augment(dataset,temp_path)
        writer("dataset processed")

def treating_augment(dataset_path, temp_path):
    from os import listdir, remove
    from os.path import join
    temp_imgs = listdir(temp_path)
    for img in temp_imgs:
        src_path = join(temp_path, img)
        dest_path = join(dataset_path, img)
        try:
            remove(dest_path)  
        except FileNotFoundError:
            pass
        finally:
            ag.image.PIL.Image.open(src_path).save(dest_path)  
    ag.utils.rmtree(temp_path)


def image_treating(image_path:str) -> None:
    from cv2 import imread,equalizeHist,GaussianBlur,imwrite,split,merge,COLOR_BGR2RGB
    image = imread(image_path)
    channels = split(image)
    eq_channels = [equalizeHist(channel) for channel in channels]
    eq_image = merge(eq_channels)
    image = eq_image
    image = GaussianBlur(image,(3,3),0)
    imwrite(image_path,image)
    
def format_dataset(dataset:str,extension:str="jpg",writer:Callable[[str],None]=print,
                   equalize_hist:bool=False):
    from PIL import Image   
    from os import listdir,remove
    from os.path import join
    
    for image in listdir(dataset):
        old_ext = image.split(".")[-1]
        image_path = join(dataset,image)
        if equalize_hist:
            image_treating(image_path)
        n = Image.open(image_path)
        n.save(image_path.replace(old_ext,extension),optimize=True)
        if old_ext != extension:
            remove(join(dataset,image))
    
    writer(f"all images formatted to {extension}")
    
def normalize(input_array, colors):
    import numpy as np
    input_shape = input_array.shape
    colors = np.array(colors)
    input_array = input_array.reshape(-1, 3)
    distances = np.linalg.norm(input_array[:, np.newaxis] - colors, axis=2)
    closest_color_indices = np.argmin(distances, axis=1)
    normalized_array = colors[closest_color_indices].reshape(input_shape)
    return normalized_array

if __name__ == "__main__":
    augment_dataset("dataset",20,file_extension="png")


