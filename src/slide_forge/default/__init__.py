from pathlib import Path

from pptx import Presentation as make_presentation
from pptx.presentation import Presentation

TEMPLATE_PATH = Path(__file__).parent / "template.pptx"
TEMPLATE_HASH = "1b3b1c97d817b02f7964ec234d39a05e26bef8dfa792313aee362625d84d3e24"


def _get_hash(path: Path) -> str:
    from hashlib import sha256

    obj = path.read_bytes()
    return sha256(obj).hexdigest()


def get_presentation() -> Presentation:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template PPTX file not found at {TEMPLATE_PATH}")
    if _get_hash(TEMPLATE_PATH) != TEMPLATE_HASH:
        raise ValueError(f"Template PPTX file hash mismatch. Expected {TEMPLATE_HASH}, got {_get_hash(TEMPLATE_PATH)}")
    return make_presentation(str(TEMPLATE_PATH))
