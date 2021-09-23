#pragma once

struct ImVec2;
namespace icons {
 struct uv { float x; float y; inline operator ImVec2 const& () const { return *reinterpret_cast<const ImVec2*>(this); } };
 struct frame { uv uv0; uv uv1; };
 struct sz16 {
   static constexpr frame infoCircle               {{0.3125000000,0.8333333333},{0.3437500000,0.9166666667}};
   static constexpr frame fileEarmark              {{0.3437500000,0.8333333333},{0.3750000000,0.9166666667}};
   static constexpr frame folderOpen               {{0.3750000000,0.8333333333},{0.4062500000,0.9166666667}};
   static constexpr frame save                     {{0.4062500000,0.8333333333},{0.4375000000,0.9166666667}};
   static constexpr frame fileImport               {{0.4375000000,0.8333333333},{0.4687500000,0.9166666667}};
   static constexpr frame fileExport               {{0.4687500000,0.8333333333},{0.5000000000,0.9166666667}};
   static constexpr frame folder                   {{0.5000000000,0.8333333333},{0.5312500000,0.9166666667}};
   static constexpr frame sliders                  {{0.5312500000,0.8333333333},{0.5625000000,0.9166666667}};
   static constexpr frame eye                      {{0.5625000000,0.8333333333},{0.5937500000,0.9166666667}};
   static constexpr frame layers                   {{0.5937500000,0.8333333333},{0.6250000000,0.9166666667}};
   static constexpr frame view_bottom              {{0.6250000000,0.8333333333},{0.6562500000,0.9166666667}};
   static constexpr frame view_front               {{0.6562500000,0.8333333333},{0.6875000000,0.9166666667}};
   static constexpr frame view_iso                 {{0.6875000000,0.8333333333},{0.7187500000,0.9166666667}};
   static constexpr frame view_left                {{0.7187500000,0.8333333333},{0.7500000000,0.9166666667}};
   static constexpr frame view_rear                {{0.7500000000,0.8333333333},{0.7812500000,0.9166666667}};
   static constexpr frame view_right               {{0.7812500000,0.8333333333},{0.8125000000,0.9166666667}};
   static constexpr frame view_top                 {{0.8125000000,0.8333333333},{0.8437500000,0.9166666667}};
 };
 struct sz32 {
   static constexpr frame infoCircle               {{0.1250000000,0.6666666667},{0.1875000000,0.8333333333}};
   static constexpr frame fileEarmark              {{0.1875000000,0.6666666667},{0.2500000000,0.8333333333}};
   static constexpr frame folderOpen               {{0.2500000000,0.6666666667},{0.3125000000,0.8333333333}};
   static constexpr frame save                     {{0.3125000000,0.6666666667},{0.3750000000,0.8333333333}};
   static constexpr frame fileImport               {{0.3750000000,0.6666666667},{0.4375000000,0.8333333333}};
   static constexpr frame fileExport               {{0.4375000000,0.6666666667},{0.5000000000,0.8333333333}};
   static constexpr frame folder                   {{0.5000000000,0.6666666667},{0.5625000000,0.8333333333}};
   static constexpr frame sliders                  {{0.5625000000,0.6666666667},{0.6250000000,0.8333333333}};
   static constexpr frame eye                      {{0.6250000000,0.6666666667},{0.6875000000,0.8333333333}};
   static constexpr frame layers                   {{0.6875000000,0.6666666667},{0.7500000000,0.8333333333}};
   static constexpr frame view_bottom              {{0.7500000000,0.6666666667},{0.8125000000,0.8333333333}};
   static constexpr frame view_front               {{0.8125000000,0.6666666667},{0.8750000000,0.8333333333}};
   static constexpr frame view_iso                 {{0.8750000000,0.6666666667},{0.9375000000,0.8333333333}};
   static constexpr frame view_left                {{0.9375000000,0.6666666667},{1.0000000000,0.8333333333}};
   static constexpr frame view_rear                {{0.1250000000,0.8333333333},{0.1875000000,1.0000000000}};
   static constexpr frame view_right               {{0.1875000000,0.8333333333},{0.2500000000,1.0000000000}};
   static constexpr frame view_top                 {{0.2500000000,0.8333333333},{0.3125000000,1.0000000000}};
 };
 struct sz64 {
   static constexpr frame infoCircle               {{0.0000000000,0.0000000000},{0.1250000000,0.3333333333}};
   static constexpr frame fileEarmark              {{0.1250000000,0.0000000000},{0.2500000000,0.3333333333}};
   static constexpr frame folderOpen               {{0.2500000000,0.0000000000},{0.3750000000,0.3333333333}};
   static constexpr frame save                     {{0.3750000000,0.0000000000},{0.5000000000,0.3333333333}};
   static constexpr frame fileImport               {{0.5000000000,0.0000000000},{0.6250000000,0.3333333333}};
   static constexpr frame fileExport               {{0.6250000000,0.0000000000},{0.7500000000,0.3333333333}};
   static constexpr frame folder                   {{0.7500000000,0.0000000000},{0.8750000000,0.3333333333}};
   static constexpr frame sliders                  {{0.8750000000,0.0000000000},{1.0000000000,0.3333333333}};
   static constexpr frame eye                      {{0.0000000000,0.3333333333},{0.1250000000,0.6666666667}};
   static constexpr frame layers                   {{0.1250000000,0.3333333333},{0.2500000000,0.6666666667}};
   static constexpr frame view_bottom              {{0.2500000000,0.3333333333},{0.3750000000,0.6666666667}};
   static constexpr frame view_front               {{0.3750000000,0.3333333333},{0.5000000000,0.6666666667}};
   static constexpr frame view_iso                 {{0.5000000000,0.3333333333},{0.6250000000,0.6666666667}};
   static constexpr frame view_left                {{0.6250000000,0.3333333333},{0.7500000000,0.6666666667}};
   static constexpr frame view_rear                {{0.7500000000,0.3333333333},{0.8750000000,0.6666666667}};
   static constexpr frame view_right               {{0.8750000000,0.3333333333},{1.0000000000,0.6666666667}};
   static constexpr frame view_top                 {{0.0000000000,0.6666666667},{0.1250000000,1.0000000000}};
 };
}
