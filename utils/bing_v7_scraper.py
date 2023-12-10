import requests
from typing import List
import os

def v7_images_search(search_term:str,azure_key:str,count:int=150,offset:int=0) -> dict:
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    subscription_key = azure_key
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term,"count":count,"imageType":"Photo","offset":offset,"safeSearch":"Strict"}
    response = requests.get(search_url,headers=headers,params=params)
    response.raise_for_status()
    
    return response.json()

def filter_value_arr(filters:List[str],value_array:List[dict],valid_extensions=[".jpg",".png"]) -> list:
    in_filters = lambda string : any(map(lambda i:i in string,filters)) 
    ext_filters = lambda string: any(ext in string.lower() for ext in valid_extensions)
    filtered_array = [] 
    for value in value_array:
        image_url = value["contentUrl"]
        if not in_filters(image_url) and ext_filters(image_url):
            filtered_array.append(image_url)
    return filtered_array

def download_images(images_link: list, folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, image_url in enumerate(images_link):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            file_extension = image_url.split(".")[-1][:3]
            image_path = os.path.join(folder, f"image_{i+1}.{file_extension}")
            
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        except Exception as e:
            print(f"Error downloading image {i+1}: {str(e)}")


if __name__ == "__main__":
    filters = ["bigstockphoto","alamy","istockphoto","dreamstime","shutterstock"
               "blogspot","gif","jpe"]
    with open("key.txt","r") as k:
        key = k.readline().strip() 
    
    wanted_images = 200     
    count = 100
    search_term = "ship draft mark"
    filtered_image = []
    offset = None
    
    while (len(filtered_image) < wanted_images):
        aux_offset = 0 if offset == None else offset 
        result_dict = v7_images_search(search_term,key,count=count,offset=aux_offset)
        offset = result_dict["nextOffset"]
        filtered_image.extend(filter_value_arr(filters,result_dict["value"]))
    
    download_images(images_link=filtered_image,folder="dataset")