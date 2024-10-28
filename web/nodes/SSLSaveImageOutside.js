import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Comfy.SSLSaveImageOutside",
    async nodeCreated(node) {
        if (node.comfyClass === "SSLSaveImageOutside") {
            node.addWidget("preview", "");
        }
    }
});