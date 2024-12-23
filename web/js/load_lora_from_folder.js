import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "QHNodes.LoadLoraFromFolder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LoadLoraFromFolder") {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (this.widgets) {
                    const pos = this.widgets.findIndex((w) => w.name === "lora_list");
                    if (pos !== -1) {
                        for (let i = pos; i < this.widgets.length; i++) {
                            this.widgets[i].onRemove?.();
                        }
                        this.widgets.length = pos;
                    }
                }

                // Create a new readonly textbox to display LoRA list
                const widget = ComfyWidgets["STRING"](this, "lora_list", ["STRING", { multiline: true }], app).widget;
                widget.inputEl.readOnly = true;
                widget.inputEl.style.opacity = 0.6;
                
                // If there are returned loras, format and display them
                if (message.loras && Array.isArray(message.loras[0])) {
                    const loraFiles = message.loras[0];
                    const formattedList = loraFiles.map(path => {
                        // Extract filename from path
                        const fileName = path.split('/').pop();
                        return fileName;
                    }).join('\n');
                    widget.value = formattedList || "No LoRA files found";
                } else {
                    widget.value = "No LoRA files found";
                }

                this.onResize?.(this.size);
            };
        }
    }
});