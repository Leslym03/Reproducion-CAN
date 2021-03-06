import numpy as np
from PIL import Image

############ get image ##################
def get_image(image_path, input_height, input_width, resize_height=64, resize_width=64, crop=False):
    image = imread(image_path)
    return transform(image, input_height, input_width, resize_height, resize_width, crop)


def imread(path):
    return Image.open(path)


def transform(image, input_height, input_width, resize_height=64, resize_width=64, crop=False):
    """
    Transforming image from range [0 255] to [-1 1]
    :param image:
    :param input_height:
    :param input_width:
    :param resize_height:
    :param resize_width:
    :param crop:
    :return:
    """
    cropped_image = image.resize((resize_width, resize_height))
    cropped_array = np.asarray(cropped_image) / 127.5 - 1.

    if cropped_array.shape == (input_height, input_width):
        cropped_array = np.stack((cropped_array,) * 3, axis=-1)
    elif cropped_array.shape[2] > 3:
        print('Array Shape :', cropped_array.shape)
        print(image.filename)
        cropped_array = cropped_array[:, :, :3]
    elif cropped_array.shape[2] < 3:
        print('Array shape :', cropped_array.shape)
        print(image.filename)
        cropped_array = cropped_array[:, :, 0]
        cropped_array = np.stack((cropped_array,) * 3, axis=-1)

    return cropped_array


############# save image ############
def save_images(images, size, image_path):
    return imsave(inverse_transform(images), size, image_path)


def inverse_transform(images):
    """
    Change image from range [-1 1] to [0 1]
    :param images:
    :return:
    """
    return (images + 1.) / 2.


def imsave(images, size, path):
    array = np.squeeze(merge(images, size))
    print("Sample image array dtype: ", array.dtype)
    img = (255 * array).astype(np.uint8)
    image = Image.fromarray(img)
    return image.save(path)


def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    if images.shape[3] in (3, 4):
        c = images.shape[3]
        img = np.zeros((h * size[0], w * size[1], c))
        for idx, image in enumerate(images):
            i = idx % size[1]
            j = idx // size[1]
            img[j * h:j * h + h, i * w:i * w + w, :] = image
    else:
        raise ValueError('in merge(images,size) images parameter '
                         'must have dimensions: HxW or HxWx3 or HxWx4')
    return img


######## Get Image Size ################
def image_manifold_size(num_images):
    # manifold_h = int(np.floor(np.sqrt(num_images)))
    # manifold_w = int(np.ceil(np.sqrt(num_images)))
    manifold_h = int(num_images) // 4
    manifold_w = 4
    assert manifold_h * manifold_w == num_images
    return manifold_h, manifold_w


def save_single_image(img_array, filename):
    img_array = np.squeeze(img_array)
    img_array = inverse_transform(img_array)
    img_array = (255 * img_array).astype(np.uint8)
    img = Image.fromarray(img_array)
    img.save(filename)