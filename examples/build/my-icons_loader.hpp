#pragma once

#include <imgui.h>
#include "my-icons.hpp"
#include "my-icons_codes.hpp"

namespace icons {
 namespace Font {
  static const ImWchar ranges[] = { icons::Font_StartCode , icons::Font_EndCode, 0 };
  inline ImFont* Load(ImGuiIO& io, const float size, ImFontConfig* config) {
   void* data = const_cast<unsigned int*>(icons::data::DATA);
   if (config) {
    config->FontDataOwnedByAtlas = false;
    return io.Fonts->AddFontFromMemoryTTF(data, icons::data::SIZE, size, config, ranges);
   }
   else {
    ImFontConfig dconf;
    dconf.FontDataOwnedByAtlas = false;
    return io.Fonts->AddFontFromMemoryTTF(data, icons::data::SIZE, size, &dconf, ranges);
   }
  }
 }
}
