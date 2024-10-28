import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "comfy.SSLNodes.SSLSaveImageOutside",
    async nodeCreated(node) {
        if (node.comfyClass === "SSLSaveImageOutside") {
            node.addWidget("preview", "");
        }
    }
});