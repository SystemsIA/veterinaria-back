CKEDITOR_UPLOAD_PATH = "ckeditor/images/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_CONFIGS = {
    "default": {
        "allowedContent": True,
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "FontSize",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Subscript",
                "Superscript",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink"],
            ["Image", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            ["NumberedList", "BulletedList"],
            ["Indent", "Outdent"],
        ],
        "language": "es",
        "height": 300,
        "width": 850,
        "extraPlugins": "justify,liststyle,indent",
    },
}
