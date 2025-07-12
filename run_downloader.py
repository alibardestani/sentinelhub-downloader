from sentinel_downloader import download_sentinel_image, plot_image

bbox = [15.461282, 46.757161, 15.574922, 46.851514]
date_range = ("2022-07-01", "2022-07-20")
bands = ["B02", "B03", "B04"]

img = download_sentinel_image(
    bbox_coords=bbox,
    time_interval=date_range,
    bands=bands,
    resolution=10,
    output_base="data/s2_truecolor"
)

plot_image(img, "True Color Sentinel-2 Image")
