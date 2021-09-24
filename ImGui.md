# BAWR

How to use BAWR with ImGui

## ImGui Example `config.py`

```python
from bawr.config import *

class Env( Environment ):
    pass

class BootstrapIcons( IconSet ):
    src = 'bootstrap-icons'
    select = [
        ('info-circle',              'infoCircle'),
        ('file-earmark',             'fileEarmark'),
        ('folder2-open',             'folderOpen'),
        ('hdd',                      'save'),
        ('file-earmark-arrow-up',    'fileImport'),
        ('file-earmark-arrow-down',  'fileExport'),
        ('folder',                   'folder'),
        ('sliders',                  'sliders'),
        ('eye',                      'eye'),
        ('layers',                   'layers'),
    ]
    options = {
        "font_transformation": [('scale', 0.75, 0.75)],
        "atlas_preprocessors": [
            RegexReplacePreprocessor(
                {
                    "currentColor": "#ffffff",
                    'width="1em"': 'width="16"',
                    'height="1em"': 'height="16"',
                }            
            )
        ],
        "atlas_margin": 0.0625
    }

class MyIcons( IconSet ):
    src = 'icons'
    options = {
        "atlas_preprocessors": [
            RegexReplacePreprocessor(
                {
                    'fill:#000000': "fill:#ffffff",
                    'stroke:#000000': 'stroke:#ffffff',
                }            
            )
        ]
    }

class MyFont( Font ):
    copyright = "Copyright 2020 Frank D. Martinez M."
    name = "my-icons"
    family = "my-icons"
    collections = (BootstrapIcons, MyIcons)

class MyCppFontH( CppFontHeader ):
    source = MyFont    
    constexpr = True
    namespace = "my_icons"

class MyCppFontEmbed( CppEmbedded ):
    source = "${BAWR_OUTPUT_DIR}/my-icons.ttf"
    namespace = "my_icons"

class MyCppFontImGui( ImGuiFontLoader ):
    font = MyFont
    header = MyCppFontH    
    data = MyCppFontEmbed 

class MyAtlas( Atlas ):
    width = 512
    sizes = (16, 32, 64)
    collections = (BootstrapIcons, MyIcons)

class MyCppAtlasEmbed( CppEmbedded ):
    source = "${BAWR_OUTPUT_DIR}/atlas.png"
    namespace = "my_atlas"

class MyAtlasHeader( CppAtlasHeader ):
    source = MyAtlas


```


## Usage with Generic Multi size Atlas (without font)

Copy the generated files to your project

- atlas.cpp
- atlas.hpp
- atlas_cells.hpp

Be sure to include any .cpp in your compilation.

### ImGui code

Texture loading is backend dependent so use the embedded data with your own texture loader.

```cpp

// During ImGui Init ...

#include "atlas.hpp" // provides my_atlas namespace 

ImTextureID textureId = load_texture_with_your_backend_loader( 
    my_atlas::data::DATA, 
    my_atlas::data::SIZE 
);

// During ImGui render ...

#include "atlas_cells.hpp" // provides icons namespace

ImVec2 sz32{32,32};
ImGui::Image(textureId, sz32, icons::sz32::fileExport.uv0, icons::sz32::fileExport.uv1);

ImVec2 sz16{16,16};
ImGui::Image(textureId, sz16, icons::sz16::fileExport.uv0, icons::sz16::fileExport.uv1);


```

## Usage with Icon Font (without generic atlas)

Copy the generated files to your project

- my-icons.cpp
- my-icons.hpp
- my-icons_codes.hpp
- my-icons_loader.hpp

Be sure to include any .cpp in your compilation.

## ImGui code

```cpp
// During ImGui Init ...

#include "my-icons_loader.hpp" // provides namespace icons

ImGuiIO& io = ImGui::GetIO();

// First load your normal Text font
io.Fonts->AddFontFromFileTTF("/wherever/Arial.ttf", 32);

// Then merge the icons
ImFontConfig cfg;
cfg.MergeMode = false;
cfg.PixelSnapH = true;
icons::Font::Load(ImGui::GetIO(), 32, &cfg);


// During ImGui Render ...

#include "my-icons_codes.hpp" // provides namespace my_icons

ImGui::Text("This is a text with icons %s ...", my_icons::folderOpen);

```

## Bonus: CMakeList for automatic build time generation


```cmake

# assuming you already have `imgui` target defined somewhere else.

# include svg files as sources so any change in svg file will trigger the generators.
file(GLOB SVG_SOURCES 
    ${CMAKE_CURRENT_LIST_DIR}/icons/icons/*.svg
    ${CMAKE_CURRENT_LIST_DIR}/icons/bootstrap-icons/*.svg
)

# include all generated files in compilation
set(GENERATED_SOURCES
    ${CMAKE_CURRENT_BINARY_DIR}/generated/my-icons.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/generated/atlas.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/generated/atlas.hpp
    ${CMAKE_CURRENT_BINARY_DIR}/generated/atlas_cells.hpp
    ${CMAKE_CURRENT_BINARY_DIR}/generated/my-icons.hpp
    ${CMAKE_CURRENT_BINARY_DIR}/generated/my-icons_codes.hpp
    ${CMAKE_CURRENT_BINARY_DIR}/generated/my-icons_loader.hpp
)

# Here is the magic. BAWR command
add_custom_command(
    OUTPUT ${GENERATED_SOURCES}
    COMMAND python3 -m bawr.tool --out "${CMAKE_CURRENT_BINARY_DIR}/generated" --src "${CMAKE_CURRENT_LIST_DIR}/icons" --cfg "${CMAKE_CURRENT_LIST_DIR}/icons/config.py"
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/icons
    DEPENDS 
        ${SVG_SOURCES} 
        ${CMAKE_CURRENT_LIST_DIR}/icons/config.py
    COMMENT "Compiling svg icons to embedded assets"
)

# custom assets target
add_custom_target(assets
  DEPENDS
    ${GENERATED_SOURCES}
  COMMENT "Running assets")

# your target
add_executable(demo
    src/demo.cpp
    ${GENERATED_SOURCES}
)

add_dependencies(demo assets)

target_include_directories(demo
    PRIVATE 
        ${CMAKE_CURRENT_BINARY_DIR}/generated
        src
)

target_link_libraries(demo
    imgui
)
```