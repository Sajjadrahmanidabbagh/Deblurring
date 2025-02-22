# Deblurring
Restore sharpness in blurred images.

### This code is part of a course assignment (Image Processing for Engineers), Which I lectured in 2022. ###

**Code Description:**
This Python script demonstrates how to use a simple deep learning model based on a UNet architecture to deblur images. The program includes data preprocessing, training, and evaluation steps. Blurred and sharp image pairs are used to train the model, which learns to predict sharp images from blurred inputs. The training process optimizes the Mean Squared Error (MSE) loss between the predicted and actual sharp images, while evaluation metrics like PSNR (Peak Signal-to-Noise Ratio) and SSIM (Structural Similarity Index Measure) are used to assess the performance

**Key Libraries/Functions:**
1. OpenCV: Handles image loading and manipulation.
2. PyTorch: Implements the UNet model, optimizers, loss functions, and manages the training loop.
3. Torchvision: Provides utilities for data transformations.
4. NumPy: Used for array manipulations and metric calculations.
5. Scikit-Image: Computes evaluation metrics such as PSNR and SSIM.

**Example Applications:**
1. Medical Imaging: Restoring clarity in blurred medical scans, such as MRIs or X-rays, to improve diagnostic accuracy.
2. Autonomous Vehicles: Enhancing the clarity of images captured by cameras in low-visibility conditions to ensure safe navigation.
3. Surveillance Systems: Deblurring security footage for better identification of objects or individuals in critical scenarios.
