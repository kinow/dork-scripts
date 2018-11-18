#!/usr/bin/env python3

"""A script to iterate through directories and produce cropped images.

The images contain the video screen area of YouTube videos. The screenshots
were taken from my computer, with 900/1600 resolution, and the location is
always the same for the ROI.

Ideally a future version will automatically detect the location based on
some algorithm/strategy.

Free to use, under MIT License.
"""

import argparse
import asyncio
import logging
import os

import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input directory", dest="input_directory")
args = ap.parse_args()

logging.basicConfig(format="[%(thread)-5d]%(asctime)s: %(message)s")
logger = logging.getLogger('async')
logger.setLevel(logging.INFO)


async def crop_image(image_file, image_index, semaphore):
    """"

    :type image_file: str
    :type image_index: int
    :type semaphore: asyncio.BoundedSemaphore
    """
    async with semaphore:
        img = cv2.imread(image_file, -1)
        output_folder = os.path.dirname(image_file)
        output_file = os.path.join(output_folder, "screenshot_{}.png".format(image_index))
        logger.info("Writing file: {}".format(output_file))
        video_screenshot = img[255:760, 125:1025]
        cv2.imwrite(output_file, video_screenshot)


async def main():
    """Process directories recursively, creating cropped screen shots."""

    tasks = list()
    # semaphore to process 5 files at most
    semaphore = asyncio.BoundedSemaphore(6)

    for _, folders, _ in os.walk(args.input_directory):
        for folder in folders:
            image_index = 0
            images_folder = os.path.join(args.input_directory, folder)
            for _, _, image_files in os.walk(images_folder):  # type: str
                for image_file in image_files:
                    if os.path.isdir(os.path.join(images_folder, image_file)):
                        continue
                    if len(image_file) < len("_.___") or image_file[-4:] not in [".png", ".jpg"]:
                        continue
                    image_file = os.path.join(images_folder, image_file)
                    tasks.append(asyncio.ensure_future(crop_image(image_file, image_index, semaphore)))
                    image_index += 1

                    await asyncio.sleep(0)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    """Start main loop."""
    logger.info("Starting main loop")
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main())
    logger.info("Completed")
