# skip_update_app.spec

block_cipher = None

added_files = [
    # Add paths to additional files or directories here, if any.
    # Example: ('path/on/disk', 'path/in/exe')
]

a = Analysis(['main.py'],
             pathex=['venv/Lib/site-packages'],
             binaries=[],
             datas=added_files,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             hiddenimports=['steam'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SkipUpdateApp',  # Modify the name of the application
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,  # set to True if you want a console window to appear
          icon="icon\icon.ico"  # Modify if you have a different icon or remove if you don't have an icon
)
