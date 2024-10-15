import albumentations as A
import random

class Augmentations():
    def __init__(self, input_image, ground_truth, is_train):
        self.is_train = is_train
        self.image = input_image
        self.ground_truth = ground_truth

        transform_shape = A.Compose(
            [
                A.Resize(width = 640, height = 320),   
                A.HorizontalFlip(p = 0.5),   
            ]
        )

        transform_noise = A.Compose(
            [      
                A.ColorJitter(brightness=0.6, contrast=0.6, saturation=0.6, hue=0.2, p=0.5),
                A.GaussNoise(var_limit=(50.0, 100.0), mean=0, noise_scale_factor=0.2, p=0.5),
                A.ISONoise(color_shift=(0.1, 0.5), intensity=(0.5, 0.5), p=0.5),
                A.RandomRain(p=0.1),
                A.Spatter(mean=(0.65, 0.65), std=(0.3, 0.3), gauss_sigma=(2, 2), \
                    cutout_threshold=(0.68, 0.68), intensity=(0.3, 0.3), mode='rain', \
                    p=0.1),             
            ]
        )
        
        self.adjust_shape = transform_shape(image=self.image, \
            masks = self.ground_truth)
        
        self.augmented_image = self.adjust_shape["image"]
        self.augmented_data = self.adjust_shape["masks"]

        if (random.random() >= 0.25 and self.is_train):
            
            self.add_noise = transform_noise(image=self.augmented_image)
            self.augmented_image = self.add_noise["image"]
        
        self.getAugmentedData()

    def getAugmentedData(self):
        return self.augmented_image, self.augmented_data