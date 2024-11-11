import hashlib
import os
import time
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import requests
import json
import numpy as np
import folder_paths
from comfy.cli_args import args
import comfy.sd
import random

# 动态获取路径
dir = os.path.dirname(__file__)  # 当前脚本目录
last1 = os.path.basename(dir)  # 最后一个目录
last2 = os.path.basename(os.path.dirname(dir))  # 倒数第二个目录
gategory = f"{last2}👾👾👾/{last1}"  # 动态获取的当前文件夹路径
MAX_SEED_NUM = 1125899906842624


class SSLLoadJson:
    """load json"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "File path or url.",
                    },
                ),
            },
            "optional": {
                "load_from_url": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Load json from url."},
                ),
                "print_to_console": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Print to console."},
                ),
            },
        }

    RETURN_TYPES = (
        "JSON",
        "INT",
    )
    RETURN_NAMES = (
        "json",
        "key_count",
    )
    CATEGORY = gategory
    FUNCTION = "load_json"

    def load_json(self, file_path, load_from_url=False, print_to_console=False):
        if load_from_url:
            response = requests.get(file_path, timeout=5)
            if response.status_code != 200:
                raise Exception(response.text)
            data = response.json()
        else:
            with open(file_path, "r") as f:
                data = json.load(f)
        if print_to_console:
            print("JSON content:", json.dumps(data))
        key_count = len(data.keys())
        return (
            data,
            key_count,
        )

    @classmethod
    def IS_CHANGED(self, file_path, load_from_url=False, print_to_console=False):
        if load_from_url:
            response = requests.get(file_path, timeout=5)
            if response.status_code != 200:
                raise Exception(response.text)
            data = response.json()
        else:
            with open(file_path, "r") as f:
                data = json.load(f)
        if print_to_console:
            print("JSON content:", json.dumps(data))
        m = hashlib.sha256()
        m.update(data)
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(
        self,
        file_path,
        load_from_url=False,
    ):
        if load_from_url:
            pass
        else:
            if not folder_paths.exists_annotated_filepath(file_path):
                return "Invalid json file: {}".format(file_path)
        return True


class SSLGetJsonKeysCount:
    """get json keys count"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json": ("JSON", {"default": ""}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("key_count",)
    CATEGORY = gategory
    FUNCTION = "get_json_keys_count"

    def get_json_keys_count(self, json):
        return (len(json.keys()),)


class SSLLoadCheckpointByName:
    """load checkpoint by name string"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    OUTPUT_TOOLTIPS = (
        "The model used for denoising latents.",
        "The CLIP model used for encoding text prompts.",
        "The VAE model used for encoding and decoding images to and from latent space.",
    )

    CATEGORY = gategory
    DESCRIPTION = "Loads a diffusion model checkpoint, diffusion models are used to denoise latents."
    FUNCTION = "load_checkpoint_by_name"

    def load_checkpoint_by_name(self, name):
        ckpt_path = folder_paths.get_full_path("checkpoints", name)
        out = comfy.sd.load_checkpoint_guess_config(
            ckpt_path,
            output_vae=True,
            output_clip=True,
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
        )
        return out[:3]


class SSLRandomNumInLoop:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ("INT", {"forceInput": True}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "my_unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("num",)
    CATEGORY = gategory
    FUNCTION = "doit"

    # 总是改变seed
    @classmethod
    def IS_CHANGED(self, index, prompt=None, extra_pnginfo=None, my_unique_id=None):
        return float("NaN")

    def doit(self, index, prompt=None, extra_pnginfo=None, my_unique_id=None):
        return (random.randint(0, MAX_SEED_NUM),)


class SSLRandomSeedInLoop:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ("INT", {"forceInput": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": MAX_SEED_NUM}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "my_unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    CATEGORY = gategory
    FUNCTION = "doit"

    # 总是改变seed
    @classmethod
    def IS_CHANGED(
        self, index, seed=0, prompt=None, extra_pnginfo=None, my_unique_id=None
    ):
        return float("NaN")

    def doit(self, index, seed=0, prompt=None, extra_pnginfo=None, my_unique_id=None):
        return (seed,)


class SSLSaveImageOutside:
    """save image outside comfyui"""

    def __init__(self):
        self.output_dir = ""
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "save_to_dir": (
                    "STRING",
                    {
                        "default": "E:/SD_Images_Files/ComfyUI",
                        "tooltip": "The dir for the image to save.",
                    },
                ),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "%year%-%month%-%day%/ComfyUI_%width%x%height%",
                        "tooltip": "The prefix for the file to save. This may include formatting information such as %year%-%month%-%day% or %Empty Latent Image.width% to include values from nodes.",
                    },
                ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    CATEGORY = gategory
    DESCRIPTION = "Saves the input images to your outside directory."

    OUTPUT_NODE = True

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    RETURN_NAMES = ()

    def get_save_image_path(
        self, filename_prefix: str, output_dir: str, image_width=0, image_height=0
    ) -> tuple[str, str, int, str, str]:

        def map_filename(filename: str) -> tuple[int, str]:
            prefix_len = len(os.path.basename(filename_prefix))
            prefix = filename[: prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1 :].split("_")[0])
            except:
                digits = 0
            return digits, prefix

        def compute_vars(input: str, image_width: int, image_height: int) -> str:
            input = input.replace("%width%", str(image_width))
            input = input.replace("%height%", str(image_height))
            now = time.localtime()
            input = input.replace("%year%", str(now.tm_year))
            input = input.replace("%month%", str(now.tm_mon).zfill(2))
            input = input.replace("%day%", str(now.tm_mday).zfill(2))
            input = input.replace("%hour%", str(now.tm_hour).zfill(2))
            input = input.replace("%minute%", str(now.tm_min).zfill(2))
            input = input.replace("%second%", str(now.tm_sec).zfill(2))
            return input

        if "%" in filename_prefix:
            filename_prefix = compute_vars(filename_prefix, image_width, image_height)

        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))

        full_output_folder = os.path.join(output_dir, subfolder)

        try:
            counter = (
                max(
                    filter(
                        lambda a: os.path.normcase(a[1][:-1])
                        == os.path.normcase(filename)
                        and a[1][-1] == "_",
                        map(map_filename, os.listdir(full_output_folder)),
                    )
                )[0]
                + 1
            )
        except ValueError:
            counter = 1
        except FileNotFoundError:
            os.makedirs(full_output_folder, exist_ok=True)
            counter = 1
        return full_output_folder, filename, counter, subfolder, filename_prefix

    def save_images(
        self,
        images,
        save_to_dir="",
        filename_prefix="ComfyUI",
        prompt=None,
        extra_pnginfo=None,
    ):
        filename_prefix += self.prefix_append
        self.output_dir = save_to_dir
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            self.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        results = list()
        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(
                os.path.join(full_output_folder, file),
                pnginfo=metadata,
                compress_level=self.compress_level,
            )
            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"ui": {"images": results}}
