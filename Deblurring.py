# Author: Sajjad
# Course Project Assignment: Machine Learning 101

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

# Define a simple UNet-like architecture
class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()

        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.ReLU()
        )

        self.bottleneck = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU()
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        bottleneck = self.bottleneck(encoded)
        decoded = self.decoder(bottleneck)
        return decoded

# Dataset class for loading blurred/sharp image pairs
class DeblurDataset(Dataset):
    def __init__(self, blurred_images, sharp_images, transform=None):
        self.blurred_images = blurred_images
        self.sharp_images = sharp_images
        self.transform = transform

    def __len__(self):
        return len(self.blurred_images)

    def __getitem__(self, idx):
        blurred = cv2.imread(self.blurred_images[idx])
        sharp = cv2.imread(self.sharp_images[idx])

        if self.transform:
            blurred = self.transform(blurred)
            sharp = self.transform(sharp)

        return blurred, sharp

# Training function
def train_model(model, dataloader, criterion, optimizer, num_epochs):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for blurred, sharp in dataloader:
            blurred = blurred.to(device)
            sharp = sharp.to(device)

            optimizer.zero_grad()
            outputs = model(blurred)
            loss = criterion(outputs, sharp)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(dataloader):.4f}")

    return model

# Evaluation function
def evaluate_model(model, blurred_images, sharp_images, transform):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    psnr_values, ssim_values = [], []

    for blurred_path, sharp_path in zip(blurred_images, sharp_images):
        blurred = cv2.imread(blurred_path)
        sharp = cv2.imread(sharp_path)

        if transform:
            blurred = transform(blurred).unsqueeze(0).to(device)

        with torch.no_grad():
            predicted = model(blurred)
            predicted = predicted.cpu().squeeze(0).numpy().transpose(1, 2, 0)

        psnr_values.append(psnr(sharp, predicted))
        ssim_values.append(ssim(sharp, predicted, multichannel=True))

    print(f"Average PSNR: {np.mean(psnr_values):.2f}")
    print(f"Average SSIM: {np.mean(ssim_values):.2f}")

# Example usage
if __name__ == "__main__":
    # File paths (update with your dataset paths)
    blurred_paths = ["blurred1.jpg", "blurred2.jpg"]
    sharp_paths = ["sharp1.jpg", "sharp2.jpg"]

    # Transforms for image preprocessing
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])

    # Create dataset and dataloader
    dataset = DeblurDataset(blurred_paths, sharp_paths, transform=transform)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    # Initialize model, criterion, and optimizer
    model = UNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Train model
    trained_model = train_model(model, dataloader, criterion, optimizer, num_epochs=10)

    # Evaluate model
    evaluate_model(trained_model, blurred_paths, sharp_paths, transform)
