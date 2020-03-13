from keras_vggface.vggface import VGGFace
VGGFace_orginal_model = VGGFace(model='vgg16',pooling='max')
print(VGGFace_orginal_model.layers[-4])