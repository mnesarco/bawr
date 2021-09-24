# Copyright 2021 Frank David Martinez Muñoz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pathlib import Path

class ImGuiFontLoader:

    # Config
    font = None
    header = None
    data = None
    name = None
    namespace = 'icons'

    # Generated
    instance = None
    output = None

    def build(self, env):
        print("[ImGui Font Loader] Start ...")

        if self.font is None or self.font.instance is None:
            print(f"[ImGui Font Loader] Invalid Font (ImGuiFontLoader.font)")
            return
        if self.data is None or self.data.instance is None:
            print(f"[ImGui Font Loader] Invalid Data (ImGuiFontLoader.data)")
            return
        if self.header is None or self.header.instance is None:
            print(f"[ImGui Font Loader] Invalid Header (ImGuiFontLoader.header)")
            return

        instance = self.data.instance
        build_dir = env.BAWR_OUTPUT_DIR
        namespace = self.namespace or self.instance.namespace

        header_file = Path(build_dir, self.name or instance.name + "_loader.hpp")
        print(f"[ImGui Font Loader] {str(header_file)}")

        data_header_file = instance.output_header        
        with open(header_file, 'w') as f:
            f.write( "#pragma once\n\n")
            f.write(f'#include <imgui.h>\n')
            f.write(f'#include "{data_header_file.name}"\n')
            f.write(f'#include "{self.header.instance.output.name}"\n\n')
            f.write(f"namespace {namespace} {{\n")
            f.write( " namespace Font {\n")
            f.write(f"  static const ImWchar ranges[] = {{ {self.header.instance.namespace}::Font_StartCode , {self.header.instance.namespace}::Font_EndCode, 0 }};\n")
            f.write( "  inline ImFont* Load(ImGuiIO& io, const float size, ImFontConfig* config) {\n")
            f.write(f"   void* data = const_cast<unsigned int*>({self.header.instance.namespace}::data::DATA);\n")
            f.write( "   if (config) {\n")
            f.write( "    config->FontDataOwnedByAtlas = false;\n")
            f.write(f"    return io.Fonts->AddFontFromMemoryTTF(data, {self.header.instance.namespace}::data::SIZE, size, config, ranges);\n")
            f.write( "   }\n")
            f.write( "   else {\n")
            f.write( "    ImFontConfig dconf;\n")
            f.write( "    dconf.FontDataOwnedByAtlas = false;\n")
            f.write(f"    return io.Fonts->AddFontFromMemoryTTF(data, {self.header.instance.namespace}::data::SIZE, size, &dconf, ranges);\n")
            f.write( "   }\n")
            f.write( "  }\n")
            f.write( " }\n")
            f.write( "}\n")

        self.output = header_file