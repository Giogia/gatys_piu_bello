import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.eager as tfe

import CNN
import Image
import Loss


def image_style_transfer(content_path, style_path, output_path, iterations=1000, content_weight=1e0, style_weight=1e2, learning_rate=5):

    #create images
    content = Image.load_image(content_path)
    style = Image.load_image(style_path)
    noise = Image.generate_noise_image(content)

    content = Image.preprocess_image(content)
    style = Image.preprocess_image(style)
    noise = Image.preprocess_image(noise)
    percentage = 0
    noise = percentage * noise + (1 - percentage) * content

    noise = tfe.Variable(noise, dtype=tf.float32)

    # create model
    vgg = CNN.VGG19_c()
    loss_weights = content_weight, style_weight
    layers_number = vgg.content_layers_num , vgg.style_layers_num

    #create features
    content_features = vgg.get_content_features(content)
    style_features = vgg.get_style_features(style)
    gram_matrix_features = [Loss.g_matrix(feature) for feature in style_features]

    img_features = content_features, gram_matrix_features

    #create optimizer
    opt = tf.train.AdamOptimizer(learning_rate, beta1=0.99, epsilon=1e-1)

    #store best results
    best_loss, best_img = float('inf'), None

    #plt.ion()
    for i in range(iterations):

        grads, loss = Loss.compute_gradient(noise,vgg.get_output_features,img_features,loss_weights,layers_number)

        opt.apply_gradients([(grads, noise)])

        clipped = Image.clip_image(noise)
        noise.assign(clipped)


        if loss < best_loss:

            # Update best loss and best image from total loss.
            best_loss = loss
            best_img = Image.postprocess_image(noise.numpy())

        if i %100 == 0:
            print("Current Loss:" +str(loss.numpy())+"  Best Loss:"+str(best_loss.numpy()))
            plot_img = noise.numpy()
            plot_img = Image.postprocess_image(plot_img)
            Image.show_image(plot_img)
            plt.show()

    Image.save_image(output_path,best_img)

    return best_loss, best_img