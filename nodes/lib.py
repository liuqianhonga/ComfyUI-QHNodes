class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

ANY = AnyType("*")

# Common variables for image processing
IMAGE_EXTENSIONS = ('*.png', '*.jpg', '*.jpeg', '*.webp')

# Common file types for saving
FILE_TYPES = [
    "txt",
    "json",
    "csv",
    "md",
    "py",
    "html",
    "css",
    "js",
    "xml",
    "yaml",
    "ini",
    "log",
    "conf",
]
