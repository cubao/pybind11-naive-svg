// should sync
// -
// https://github.com/cubao/pybind11-naive-svg/blob/master/src/pybind11_naive_svg.cpp
// -
// https://github.com/cubao/headers/tree/main/include/cubao/pybind11_naive_svg.hpp

#pragma once

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#include "cubao_inline.hpp"
#include "naive_svg.hpp"

namespace cubao
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

using RowVectorsNx2 = Eigen::Matrix<double, Eigen::Dynamic, 2, Eigen::RowMajor>;

// TODO, 各个类型的 from/to_json
// svg 的 load/dump
// svg extra attributes

CUBAO_INLINE void bind_naive_svg(py::module &m)
{
    // https://github.com/gagan-bansal/geojson2svg
    // https://milevski.co/geojson2svg/demo/lands.svg
    // 还是转化到 ENU 下，更好。radius 的尺度是一致的, stroke 也更好调

#define SETUP_FLUENT_API_PYBIND(Klass, VarType, VarName)                       \
    .def(#VarName, [](const Klass &self) { return self.VarName(); })           \
        .def(                                                                  \
            #VarName,                                                          \
            [](Klass &self, const VarType &v) { return self.VarName(v); },     \
            rvp::reference_internal)

    using Color = SVG::Color;
    py::class_<Color>(m, "Color",
                      py::module_local()) //
        .def(py::init<int>(), "rgb"_a = -1)
        .def(py::init<int, int, int, float>(), "r"_a, "g"_a, "b"_a,
             "a"_a = -1.f)
        .def("r", [](const Color &self) { return self.r(); })
        .def(
            "r", [](Color &self, int r) { return self.r(r); },
            rvp::reference_internal) //
        SETUP_FLUENT_API_PYBIND(Color, int, g)
            SETUP_FLUENT_API_PYBIND(Color, int, b)
                SETUP_FLUENT_API_PYBIND(Color, float, a)
        .def("invalid", &Color::invalid)
        .def("to_string", &Color::to_string)
        .def_static("parse",
                    [](const std::string &text) {
                        int i = text.size() - 6;
                        if (i < 0) {
                            return Color();
                        }
                        return Color(
                            std::stoi(text.substr(i, 2), nullptr, 16),
                            std::stoi(text.substr(i + 2, 2), nullptr, 16),
                            std::stoi(text.substr(i + 4, 2), nullptr, 16));
                    })
        //
        ;

    using Polyline = SVG::Polyline;
    py::class_<Polyline>(m, "Polyline",
                         py::module_local()) //
        .def(py::init([](const Eigen::Ref<const RowVectorsNx2> &points) {
                 std::vector<SVG::PointType> _(points.rows());
                 Eigen::Map<RowVectorsNx2>(&_[0][0], points.rows(), 2) = points;
                 return new SVG::Polyline(_);
             }),
             "points"_a)
        //
        SETUP_FLUENT_API_PYBIND(Polyline, Color, stroke)
            SETUP_FLUENT_API_PYBIND(Polyline, double, stroke_width)
                SETUP_FLUENT_API_PYBIND(Polyline, Color, fill)
        //
        ;

    using Polygon = SVG::Polygon;
    py::class_<>(m, "Polygon", py::module_local()) //
                                                   //
                                                   //
        .def(py::init([](const Eigen::Ref<const RowVectorsNx2> &points) {
                 std::vector<SVG::PointType> _(points.rows());
                 Eigen::Map<RowVectorsNx2>(&_[0][0], points.rows(), 2) = points;
                 return new SVG::Polygon(_);
             }),
             "points"_a) //
        SETUP_FLUENT_API_PYBIND(Polygon, Color, stroke)
            SETUP_FLUENT_API_PYBIND(Polygon, double, stroke_width)
                SETUP_FLUENT_API_PYBIND(Polygon, Color, fill)
        //
        ;

    using Circle = SVG::Circle;
    py::class_<Circle>(m, "Circle", py::module_local()) //
        .def(py::init([](const Eigen::Vector2d &center, double r) {
                 return new SVG::Circle({center[0], center[1]}, r);
             }),
             "center"_a, "r"_a = 1.0) //
        SETUP_FLUENT_API_PYBIND(Circle, Color, stroke)
            SETUP_FLUENT_API_PYBIND(Circle, double, stroke_width)
                SETUP_FLUENT_API_PYBIND(Circle, Color, fill)
        //
        ;
    py::class_<SVG::Text>(m, "Text", py::module_local()) //
                                                         //
        ;

    py::class_<SVG>(m, "SVG", py::module_local())
        .def(py::init<double, double>(), "width"_a, "height"_a)
        //
        ;
}
} // namespace cubao
