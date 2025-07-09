import re
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from core.services.auth import require_role

router = APIRouter(tags=["Changelog"])

CHANGELOG_PATH = Path(__file__).parent.parent.parent.parent / "CHANGELOG.md"


def parse_changelog(content: str) -> List[Dict]:
    """Parse markdown changelog into structured data"""
    entries = []
    current_version = None

    for line in content.split("\n"):
        if line.startswith("## ["):
            # Parse version and date
            version_match = re.match(
                r"## \[([^\]]+)\](?: - (\d{4}-\d{2}-\d{2}))?", line
            )
            if version_match:
                current_version = {
                    "version": version_match.group(1),
                    "date": version_match.group(2),
                    "changes": {"added": [], "changed": [], "fixed": [], "removed": []},
                }
                entries.append(current_version)
        elif line.startswith("### ") and current_version:
            # Parse change type
            change_type = line[4:].lower()
        elif line.startswith("- ") and current_version:
            # Parse change item
            if change_type in current_version["changes"]:
                current_version["changes"][change_type].append(line[2:])

    return entries


@router.get("", response_class=PlainTextResponse)
async def get_changelog(current_user=Depends(require_role("Admin", "Staff"))):
    """Return raw markdown changelog"""
    return CHANGELOG_PATH.read_text()


@router.get("/json")
async def get_changelog_json(current_user=Depends(require_role("Admin", "Staff"))):
    """Return parsed changelog as JSON"""
    changelog = parse_changelog(CHANGELOG_PATH.read_text())
    return JSONResponse(content=changelog)


@router.get("/latest")
async def get_latest_changelog(current_user=Depends(require_role("Admin", "Staff"))):
    """Return only the most recent changelog entry"""
    changelog = parse_changelog(CHANGELOG_PATH.read_text())
    return JSONResponse(content=changelog[0] if changelog else {})
