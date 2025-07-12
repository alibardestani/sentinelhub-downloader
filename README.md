# SentinelHub Downloader

A Python module for downloading, visualizing, and saving Sentinel-2 satellite images using the Copernicus Sentinel Hub API.

## 🚀 Features

- Download Sentinel-2 L2A data for any bounding box and time range
- Select any bands (e.g., B02, B03, B04 for true color)
- Output formats: `.npy`, `.jpg`, `.tif`
- Automatic image normalization for 8-bit / 12-bit images
- Mosaic from multiple dates (ready for extension)
- RGB visualization using `matplotlib`
- Optional `.env`-based configuration
- Easily extensible for command-line usage (CLI)

## 🛠 Installation

```bash
git clone https://github.com/alibarestani/sentinelhub-downloader.git
cd sentinelhub-downloader
pip install -r requirements.txt
