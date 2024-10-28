from .nodes.nodes import (
    SSLLoadJson,
    SSLGetJsonKeysCount,
    SSLLoadCheckpointByName,
    SSLButtonNode,
    SSLSaveImageOutside,
)

# （必填）填写 import的类名称，命名需要唯一，key或value与其他插件冲突可能引用不了。这是决定是否能引用的关键。
# key(自定义):value(import的类名称)
NODE_CLASS_MAPPINGS = {
    "SSLLoadJson": SSLLoadJson,
    "SSLGetJsonKeysCount": SSLGetJsonKeysCount,
    "SSLLoadCheckpointByName": SSLLoadCheckpointByName,
    "SSLButtonNode": SSLButtonNode,
    "SSLSaveImageOutside": SSLSaveImageOutside,
}


# （可不写）填写 ui界面显示名称，命名会显示在节点ui左上角，如不写会用类的名称显示在节点ui上
# key(自定义):value(ui显示的名称)
NODE_DISPLAY_NAME_MAPPINGS = {
    "SSLLoadJson": "SSL Load Json",
    "SSLGetJsonKeysCount": "SSL Get Json Keys Count",
    "SSLLoadCheckpointByName": "SSL Load Checkpoint By Name",
    "SSLButtonNode": "SSL Button Node",
    "SSLSaveImageOutside": "SSL Save Image Outside",
}

WEB_DIRECTORY = "./web"
# 引入以上两个字典的内容
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
