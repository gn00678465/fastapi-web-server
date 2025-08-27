from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def setup_static_dirs(app: FastAPI, base_url: str, static_dir: str) -> None:
    """
    掛載靜態資源
    """
    static_path = Path(static_dir)

    if not static_path.exists():
        raise ValueError(f"靜態檔案目錄不存在: {static_dir}")
    
    # 掛載所有靜態資源目錄
    static_subdirs = ["_nuxt", "_fonts"]
    
    app.mount(
        base_url,
        StaticFiles(directory=Path(static_dir)),
        name="spa"
    )
    
    for subdir in static_subdirs:
        subdir_path = static_path / subdir
        if subdir_path.exists():
            app.mount(
                f"{base_url}/{subdir}",
                StaticFiles(directory=subdir_path),
                name=f"static_{subdir}"
            )