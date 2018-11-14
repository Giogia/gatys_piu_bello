import tensorflow as tf
import tensorflow.keras as models
from Image import preprocess_image
class VGG19:
    def __init__(self, content, style):
        tf.enable_eager_execution()  # you enable eager eecution because we want the fow to be linear

        self.content = preprocess_image(content)

        self.style = preprocess_image(style)

        # here you say where you want to take the features for the style

        self.styleLayers = ['block5_conv2']
        self.contentLayers = ['block1_conv1',
                              'block2_conv1',   # here you say where you want to take the features for the content
                              'block3_conv1',
                              'block4_conv1',
                              'block5_conv1']
        self.model = self.getModel()

        # after setting model not trainable we also set the layers not trainable

        for layer in self.model.layers:
            layer.trainable = False

        self.content = self.model(self.content)

        self.style = self.model(self.style)

        # for the content take only the content layers from 0 to len of content

        self.content = [content[0] for content in range(0, len(self.contentLayers))]

        # for style take only the style layers from len of content to len of content + len of style

        self.style = [content[0] for content in range(len(self.contentLayers),
                                                      len(self.contentLayers) + len(self.styleLayers))]



    def getModel(self):

        # we load the VGG19 pretrained with the dataset imagenet and we don't include the 3 fully connected layers on
        # top of theVGG19

        vgg = tf.keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')

        # we freeze the weights and the variables

        vgg.trainable = False  # we load the VGG19 pretrained with the dataset imagenet and we don't include the 3 fully connected layers on
        # top of theVGG19

        vgg = tf.keras.applications.vgg19.VGG19(include_top=False,   weights='imagenet')

        #we freeze the weights and the variables

        vgg.trainable = False

        style_feature = []

        for i in self.styleLayers:
            style_feature.append(vgg.get_layer(i).output)
        content_feature = []
        for i in self.contentLayers:
            content_feature.append(vgg.get_layer(i).output)

        #using the Keras API we return the model of the CNN
    

        return models.Model(vgg.input, style_feature + content_feature)










