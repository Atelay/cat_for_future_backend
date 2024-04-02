from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.config import IMAGE_TYPES, MAX_IMAGE_SIZE_MB
from src.hero.models import Hero
from src.admin.commons.base import BaseAdmin


class HeroAdmin(BaseAdmin, model=Hero):
    name_plural = "Hero"

    can_create = False
    can_delete = False

    column_labels = {
        Hero.title: "Title",
        Hero.sub_title: "Sub-title",
        Hero.left_text: "Left-text",
        Hero.right_text: "Right-text",
        Hero.media_path: "Photo",
    }
    column_exclude_list = column_details_exclude_list = [
        Hero.id,
    ]

    column_formatters = {
        Hero.media_path: MediaFormatter(),
    }
    form_files_list = [
        Hero.media_path,
    ]
    form_args = {
        "photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                ),
            ],
            "description": IMG_REQ % (1440, 883),
        },
    }
