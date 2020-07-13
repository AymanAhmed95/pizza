# useful  utility functions
def get_images_path(instance, filename):
    return "images/%s-%s" % (instance.pizza.pk, filename)
