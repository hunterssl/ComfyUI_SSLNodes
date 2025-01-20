import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "comfy.SSLNodes.SSLSaveImageOutside",
    async nodeCreated(node) {
        if (node.comfyClass === "SSLSaveImageOutside") {
            node.addWidget("preview", "");
            
            // 添加打开目录按钮
            const btn = node.addWidget("button", "打开保存目录", null, async () => {
                try {
                    // 获取当前节点的 save_to_dir 值
                    const saveToDir = node.widgets.find(w => w.name === "save_to_dir")?.value;
                    if (!saveToDir) {
                        app.ui.dialog.show("错误", "未设置保存目录");
                        return;
                    }

                    // 发送请求到后端打开目录
                    const response = await fetch(`/ssl/open_folder?path=${encodeURIComponent(saveToDir)}`);
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                } catch (error) {
                    console.error("打开目录失败", error);
                }
            });
        }
    }
});