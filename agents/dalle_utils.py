import re

from IPython.display import display
from PIL import Image

import PIL
from diskcache import Cache
from openai import OpenAI, AzureOpenAI
from PIL import Image

from autogen import Agent
from autogen.agentchat.contrib.img_utils import get_image_data, get_pil_image


def dalle_call(client: AzureOpenAI, model: str, prompt: str, size: str, quality: str, n: int, use_cache: bool = False) -> str:
    """
    Generate an image using OpenAI's DALL-E model and cache the result.

    This function takes a prompt and other parameters to generate an image using OpenAI's DALL-E model.
    It checks if the result is already cached; if so, it returns the cached image data. Otherwise,
    it calls the DALL-E API to generate the image, stores the result in the cache, and then returns it.

    Args:
        client (OpenAI): The OpenAI client instance for making API calls.
        model (str): The specific DALL-E model to use for image generation.
        prompt (str): The text prompt based on which the image is generated.
        size (str): The size specification of the image.
        quality (str): The quality setting for the image generation.
        n (int): The number of images to generate.
        use_cache (bool) : Select if cache should be used

    Returns:
    str: The image data as a string, either retrieved from the cache or newly generated.

    Note:
    - The cache is stored in a directory named '.cache/'.
    - The function uses a tuple of (model, prompt, size, quality, n) as the key for caching.
    - The image data is obtained by making a secondary request to the URL provided by the DALL-E API response.
    """
    if use_cache:
        cache = Cache(".cache/")  # Create a cache directory
        key = (model, prompt, size, quality, n)
        if key in cache:
            return cache[key]

    # If not in cache, compute and store the result
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )
    image_url = response.data[0].url
    img_data = get_image_data(image_url)
    if use_cache:
        cache[key] = img_data

    return img_data


def extract_img(agent: Agent) -> PIL.Image:
    """
    Extracts an image from the last message of an agent and converts it to a PIL image.

    This function searches the last message sent by the given agent for an image tag,
    extracts the image data, and then converts this data into a PIL (Python Imaging Library) image object.

    Parameters:
        agent (Agent): An instance of an agent from which the last message will be retrieved.

    Returns:
        PIL.Image: A PIL image object created from the extracted image data.

    Note:
    - The function assumes that the last message contains an <img> tag with image data.
    - The image data is extracted using a regular expression that searches for <img> tags.
    - It's important that the agent's last message contains properly formatted image data for successful extraction.
    - The `_to_pil` function is used to convert the extracted image data into a PIL image.
    - If no <img> tag is found, or if the image data is not correctly formatted, the function may raise an error.
    """
    last_message = agent.last_message()["content"]

    if isinstance(last_message, str):
        img_data = re.findall("<img (.*)>", last_message)[0]
    elif isinstance(last_message, list):
        # The GPT-4V format, where the content is an array of data
        assert isinstance(last_message[0], dict)
        img_data = last_message[0]["image_url"]["url"]

    pil_img = get_pil_image(img_data)
    return pil_img


def extract_prompt_content(feedback: str) -> str:
    """ Extract image generation prompt from critics feedback message """
    prompt_marker = "PROMPT:"
    try:
        start_index = feedback.index(prompt_marker) + len(prompt_marker)
        # Find the start of the content, skipping any whitespace
        while start_index < len(feedback) and feedback[start_index].isspace():
            start_index += 1
        return feedback[start_index:]
    except ValueError:
        return ""
    
def display_image(pil_image, width=800):
    """
    Display a PIL image in a Jupyter notebook with the specified width while maintaining aspect ratio.

    :param pil_image: PIL image object.
    :param width: Desired width of the displayed image.
    """
    # Calculate the new height to maintain aspect ratio
    aspect_ratio = pil_image.height / pil_image.width
    height = int(width * aspect_ratio)
    
    # Resize the image
    resized_image = pil_image.resize((width, height), Image.LANCZOS)
    
    # Display the image
    display(resized_image)
