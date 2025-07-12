import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubRequest,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType,
)
from typing import List, Tuple


def load_config(config_name: str = "ali") -> SHConfig:
    from dotenv import load_dotenv
    load_dotenv()
    config = SHConfig(config_name)

    if not config.sh_client_id or not config.sh_client_secret:
        config.sh_client_id = os.getenv("ALI_CLIENT_ID")
        config.sh_client_secret = os.getenv("ALI_CLIENT_SECRET")
        config.sh_base_url = "https://sh.dataspace.copernicus.eu"
        config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        config.save(config_name)
    return config


def normalize_image(image: np.ndarray) -> np.ndarray:
    max_val = image.max()
    if max_val <= 255:
        return image / 255.0
    elif max_val <= 4096:
        return image / 4096.0
    else:
        return image / max_val


def save_image(image: np.ndarray, path: str, format: str = "jpg"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = normalize_image(image)
    img_uint8 = (img * 255).astype(np.uint8)
    Image.fromarray(img_uint8).save(path)
    print(f" Image saved to: {path}")


def plot_image(image: np.ndarray, title: str = "Sentinel Image"):
    plt.imshow(normalize_image(image))
    plt.title(title)
    plt.axis("off")
    plt.show()


def download_sentinel_image(
    bbox_coords: List[float],
    time_interval: Tuple[str, str],
    bands: List[str] = ["B04", "B03", "B02"],
    resolution: int = 10,
    config_name: str = "ali",
    output_base: str = "data/output"
):
    config = load_config(config_name)
    bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)

    evalscript = f"""
    //VERSION=3
    function setup() {{
        return {{
            input: [{{
                bands: {bands}
            }}],
            output: {{
                bands: {len(bands)}
            }}
        }};
    }}
    function evaluatePixel(sample) {{
        return [{', '.join([f"sample.{b}" for b in bands])}];
    }}
    """

    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A.define_from(
                    name="s2l2a",
                    service_url="https://sh.dataspace.copernicus.eu"
                ),
                time_interval=time_interval,
                other_args={"dataFilter": {"mosaickingOrder": "leastCC"}}
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=size,
        config=config,
    )

    images = request.get_data()
    image = images[0]

    npy_path = f"{output_base}.npy"
    jpg_path = f"{output_base}.jpg"
    tif_path = f"{output_base}.tif"

    np.save(npy_path, image)
    save_image(image, jpg_path, "jpg")
    Image.fromarray(image.astype(np.uint16)).save(tif_path)  # TIFF 16-bit

    print(f" NPY saved: {npy_path}")
    print(f" TIFF saved: {tif_path}")
    return image
