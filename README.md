# ComfyUI-QHNodes

为 ComfyUI 开发的自定义节点集合，提供预设尺寸预设Latent、从文件夹加载LoRA，以及集成了多个常用的自定义节点。

> 所有节点均为日常所用，如有需要，可参考使用

## 包含节点

### 主仓库节点

1. **预设尺寸 (Preset Size Latent)**: 提供常用的图像尺寸预设
2. **文件夹加载LoRA (Load LoRA from Folder)**: 批量加载指定文件夹中的 LoRA 模型

### 集成的子模块

以下是集成的常用节点，如果不需要所有节点，可单独下载：

1. [字符串相关节点](https://github.com/liuqianhonga/ComfyUI-String-Helper) 
   - 字符串相关的自定义节点，提高在处理字符串时的效率和灵活性

2. [图像压缩节点](https://github.com/liuqianhonga/ComfyUI-Image-Compressor) 
   - 用于图像压缩的ComfyUI自定义节点，支持JPEG、WEBP、PNG压缩格式和参数调整

3. [Html2Image节点](https://github.com/liuqianhonga/ComfyUI-Html2Image) 
   - 提供ComfyUI网页截图、相机水印、自由模板转图片功能节点

4. [模型下载节点](https://github.com/liuqianhonga/ComfyUI-Model-Downloader) 
   - ComfyUI的模型下载节点，支持civitai和huggingface下的模型下载

## 安装方法

### 场景一：安装所有节点（推荐）

如果你想使用所有功能，可以一次性安装所有节点：

```bash
cd ComfyUI/custom_nodes/
git clone --recursive https://github.com/liuqianhonga/ComfyUI-QHNodes.git
```

### 场景二：仅安装主仓库节点

如果你只想使用预设尺寸和文件夹加载LoRA功能：

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/liuqianhonga/ComfyUI-QHNodes.git
```

### 子模块管理（可选）

1. 添加子模块：如果之前只安装了主仓库，现在想添加子模块
```bash
cd ComfyUI/custom_nodes/ComfyUI-QHNodes
git submodule init
git submodule update
```

2. 更新子模块：如果想更新子模块到最新版本
```bash
cd ComfyUI/custom_nodes/ComfyUI-QHNodes
git submodule update --remote
```

安装完成后重启 ComfyUI

## 更新说明

### 更新主仓库
```bash
cd ComfyUI/custom_nodes/ComfyUI-QHNodes
git pull
```

### 更新所有子模块
```bash
cd ComfyUI/custom_nodes/ComfyUI-QHNodes
git submodule update --remote
```

## 节点说明

### 🐟预设尺寸 (Preset Size Latent)

预设尺寸节点，支持以下预设：

#### 竖版尺寸预设

- **竖版通用 (1024×1536)**
  - 标准的 2:3 竖版比例
  - 适合壁纸和电子书封面

- **竖版高清 (1280×1536)**
  - 5:6 竖版比例
  - 适合社交平台/AI作画

- **竖版长图 (1024×2048)**
  - 1:2 竖版比例
  - 适合全身像/海报/建筑

- **竖版超清 (1536×2048)**
  - 适合精细插画/商业海报

- **竖版超长 (1080×2520)**
  - 9:21 竖版比例
  - 适合长图文/漫画

#### 横版尺寸预设

- **横版通用 (1536×1024)**
  - 3:2 横版比例
  - 适合风景/场景

- **横版宽屏 (1920×1080)**
  - 16:9 横版比例
  - 适合桌面壁纸

- **横版超宽 (2560×1080)**
  - 21:9 横版比例
  - 适合全景图

#### 手机尺寸预设

- **手机人像 16:9 (1080×1920)**
  - 适合人像/全身照
  - 标准的手机全屏比例

- **手机人像 4:3 (1440×1920)**
  - 适合证件照/半身像
  - 更宽的画面比例

- **手机场景 3:2 (1280×1920)**
  - 适合风景和建筑
  - 宽屏构图

- **手机通用 (1024×1024)**
  - 适合头像和产品图
  - 方形构图

- **手机高清 (1920×1920)**
  - 适合精致产品和艺术作品
  - 高分辨率方形

#### 视频尺寸预设

- **4K (3840×2160)**
  - 超高清视频标准
  - 适合专业视频制作

- **2K (2048×1152)**
  - 高清视频标准
  - 适合一般视频制作

- **1080p (1920×1080)**
  - 全高清视频标准
  - 最常用的视频尺寸

- **电影 (2048×870)**
  - 2.35:1 电影比例
  - 适合电影级内容

#### 相片尺寸预设

- **4×6英寸 (1200×1800)**
  - 适合冲印照片
  - 标准相片尺寸

- **5×7英寸 (1500×2100)**
  - 适合相框装饰
  - 较大相片尺寸

#### 社交媒体预设

- **抖音/快手 (1080×1920)**
  - 适合短视频封面
  - 标准竖屏比例

- **朋友圈 (1080×1920)**
  - 适合生活分享
  - 移动端优化

- **小红书 (1080×1350)**
  - 适合美食/穿搭
  - 4:5 优化比例

- **微博 (1200×900)**
  - 适合图文/新闻
  - 横版展示

- **B站封面 (1146×717)**
  - 适合视频封面
  - 平台优化尺寸

#### 国际社交平台预设

- **Instagram Story (1080×1920)**
  - 适合故事/Vlog
  - Instagram 标准尺寸

- **TikTok Video (1080×1920)**
  - 适合短视频/舞蹈
  - TikTok 优化尺寸

- **Facebook Post (1200×630)**
  - 适合社交分享
  - Facebook 推荐尺寸

- **Twitter Post (1200×675)**
  - 适合资讯/新闻
  - Twitter 优化尺寸

- **Youtube Cover (2560×1440)**
  - 适合视频封面
  - Youtube 标准尺寸

#### 自定义预设

你可以通过编辑以下文件来添加自己的预设尺寸：
- `nodes/preset_sizes.json`: 社交媒体预设
- `nodes/camera_sizes.json`: 相机预设

格式如下：
```json
{
    "预设名称 (宽×高)": [宽度, 高度]
}
```

### 🐟Load LoRA (Folder)

从指定文件夹加载 LoRA 模型。支持以下功能：

- **基础模型**：接收基础模型（MODEL）作为输入
  - 所有的 LoRA 都将基于此模型进行加载
  - 节点会自动克隆基础模型，不会修改原始模型
- **文件夹路径**：支持多个文件夹路径，使用英文逗号分隔
  - 示例：`myLoras, character/style1`
  - 相对路径基于 ComfyUI 的 `models/loras` 目录
  - 如果路径不存在会在控制台输出提示信息
- **文件过滤**：支持文件名过滤，使用英文逗号分隔多个关键词
  - 示例：`anime, style` 将只加载文件名包含 anime 或 style 的 LoRA
  - 过滤词不区分大小写
  - 留空则加载目录下所有 .safetensors 文件
- **模型强度**：调整 LoRA 对模型的影响程度
  - 范围：-100.0 到 100.0
  - 默认值：1.0
  - 负值会产生相反的效果
- **合并加载**：控制多个 LoRA 的加载方式
  - 开启：将所有符合条件的 LoRA 合并加载到同一个模型中
  - 关闭（默认）：为每个 LoRA 创建单独的模型副本
- **实时预览**：执行后会显示找到的 LoRA 文件列表，方便确认是否正确加载

#### 使用示例

1. 分别加载多个 LoRA（默认模式）：
   ```
   model: 基础模型
   lora_folders: portraits, anime/style
   filter_text: v1, quality
   strength_model: 0.8
   merge_loras: False (默认)
   ```
   输出：多个模型，每个模型包含一个 LoRA

2. 合并加载多个 LoRA：
   ```
   model: 基础模型
   lora_folders: myLoras
   filter_text: (留空)
   strength_model: 1.0
   merge_loras: True
   ```
   输出：一个包含所有 LoRA 的模型

#### 注意事项

- 文件夹路径使用正斜杠 `/` 分隔
- 目前仅支持 .safetensors 格式的 LoRA 文件
- 如果找不到任何符合条件的文件，节点会显示"No LoRA files found"
- 合并加载多个 LoRA 时，加载顺序与文件夹中的顺序一致
- 每个 LoRA 都会创建模型的副本，请注意内存使用
