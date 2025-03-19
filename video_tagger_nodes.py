import base64
import os
import shutil
from zhipuai import ZhipuAI


class MediaListNode:
    """视频/图片地址列表节点，输出目录内的媒体文件列表和对应的文本文件列表"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "file_types": (["video", "image"], {"default": "video"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    OUTPUT_IS_LIST = (True, True, False, False)
    RETURN_NAMES = ("media_path", "txt_path", "absolute_directory", "file_count")
    FUNCTION = "list_media"
    CATEGORY = "VideoTagger"
    
    def list_media(self, directory, file_types):
        if not os.path.exists(directory):
            raise ValueError(f"目录 {directory} 不存在")
        
        media_paths = []
        txt_paths = []
        
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp']
        file_count = 0
        
        allowed_extensions = []
        if file_types == "video":
            allowed_extensions.extend(video_extensions)
        if file_types == "image":
            allowed_extensions.extend(image_extensions)
        
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in allowed_extensions:
                    media_paths.append(file_path)
                    base_name = os.path.splitext(file)[0]
                    txt_path = os.path.join(directory, f"{base_name}.txt")
                    txt_paths.append(txt_path)
                    file_count += 1
        
        return (media_paths, txt_paths, directory, file_count)


class SaveMediaWithTagsNode:
    """保存节点，复制媒体文件并保存打标文本文件"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "output_directory": ("STRING", {"default": ""}),
                "media_path": ("STRING", {"default": ""}),
                "tag_content": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "save_media_with_tags"
    OUTPUT_NODE = True
    CATEGORY = "VideoTagger"
    
    def save_media_with_tags(self, output_directory, media_path, tag_content):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        if not os.path.exists(media_path):
            return f"错误：媒体文件 {media_path} 不存在"
        
        # 获取文件名和扩展名
        media_filename = os.path.basename(media_path)
        base_name = os.path.splitext(media_filename)[0]
        
        # 复制媒体文件
        output_media_path = os.path.join(output_directory, media_filename)
        # 如果文件存在，则不复制
        if not os.path.exists(output_media_path):
            shutil.copy2(media_path, output_media_path)
        
        # 保存标签文本文件
        txt_filename = f"{base_name}.txt"
        output_txt_path = os.path.join(output_directory, txt_filename)
        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(tag_content)
        
        return (f"成功：媒体文件和标签已保存到 {output_directory}",)


class Tagger_from_Glm4vPlus:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "video": ("STRING",),
            "api_key": ("STRING",),
            "role_text": ("STRING",
                          {"default": "desc video",
                           "multiline": True})
        }}

    CATEGORY = "VideoTagger"
    DESCRIPTION = "Tagger_from_Glm4vPlus"

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("text", "tokens")

    FUNCTION = "run"

    def run(self, video, role_text, api_key):
        with open(video, 'rb') as video_file:
            video_base = base64.b64encode(video_file.read()).decode('utf-8')
        client = ZhipuAI(api_key=api_key)
        response = client.chat.completions.create(
            model="glm-4v-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "video_url",
                            "video_url": {
                                "url": video_base
                            }
                        },
                        {
                            "type": "text",
                            "text": f"{role_text}"
                        }
                    ]
                }
            ]
        )

        text = ""
        tokens = 0
        if response is not None:
            if response.choices is not None and len(response.choices) > 0:
                text = response.choices[0].message.content
            if response.usage is not None and response.usage.total_tokens is not None:
                tokens = response.usage.total_tokens
        return (text, tokens,)


NODE_CLASS_MAPPINGS = {
    "MediaListNode": MediaListNode,
    "SaveMediaWithTagsNode": SaveMediaWithTagsNode,
    "Tagger_from_Glm4vPlus": Tagger_from_Glm4vPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MediaListNode": "Media List",
    "SaveMediaWithTagsNode": "Save Media with Tags",
    "Tagger_from_Glm4vPlus": "Tagger from Glm4vPlus"
} 