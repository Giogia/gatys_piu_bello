import tensorflow as tf
import os
from Image import show_content_style, show_image
from pathlib import Path
from ImageStyleTransfer import image_style_transfer
from VideoStyleTransfer import video_style_transfer

PATH = os.getcwd()
IMAGES_PATH = PATH + '/Images'
VIDEOS_PATH = PATH + '/Videos'
MODELS_PATH = PATH + '/Models'
RESULTS_PATH = PATH + '/Results'


def find_file(filename, directory):
    for file in os.listdir(directory):
        if os.path.splitext(file)[0] == filename:
            return file

    raise Exception("File not found")


if __name__ == "__main__":

    tf.enable_eager_execution()
    print("Eager execution: {}".format(tf.executing_eagerly()))

    choice = input("Select one of the following options:\n"
                    "1 - Style Transfer for Images\n"
                    "2 - Style Transfer for Videos\n")


    if choice == '1':

        print("Select Content Image:")

        for file in os.listdir(Path(IMAGES_PATH)):
            print(os.path.splitext(file)[0])

        content = find_file(input(),Path(IMAGES_PATH))
        content_path  = Path(IMAGES_PATH + "/" + content)

        print("Select Style Image:")

        for file in os.listdir(Path(IMAGES_PATH)):
            print(os.path.splitext(file)[0])

        style = find_file(input(),Path(IMAGES_PATH))
        style_path = Path(IMAGES_PATH + "/" + style)

        output =  'Result' + '_' + os.path.splitext(content)[0] + '_' + os.path.splitext(style)[0]
        output_path = Path(RESULTS_PATH + "/" + output + ".jpg")


        show_content_style(content_path, style_path)

        print("Please wait, ignore tensorflow binary value warning")
        best_loss, best_img = image_style_transfer(content_path, style_path, output_path, iterations=3)

        print("Final Loss: " + str(best_loss.numpy()))
        show_image(best_img, output)

        print("image saved in Results folder")


    if choice == '2':

        print("Select Content Video:")

        for file in os.listdir(Path(VIDEOS_PATH)):
            print(os.path.splitext(file)[0])

        content = find_file(input(),Path(VIDEOS_PATH))
        content_path  = Path(VIDEOS_PATH + "/" + content)

        print("Select Style Model:")

        for file in os.listdir(Path(MODELS_PATH)):
            print(os.path.splitext(file)[0])

        model = find_file(input(),Path(MODELS_PATH))
        model_path = Path(MODELS_PATH + "/" + model)

        output =  'Result' + '_' + os.path.splitext(content)[0] + '_' + os.path.splitext(model)[0]
        output_path = Path(RESULTS_PATH + "/" + output + ".mp4")

        print("Please wait, ignore tensorflow binary value warning")
        video_style_transfer(str(content_path), str(model_path), str(output_path), batch_s=4)

        print("video saved in Results folder")


