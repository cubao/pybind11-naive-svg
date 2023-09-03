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
    py::class_<SVG::Polyline>(
        m, "Polyline",
        py::module_local()) //
                            // .def(py::init([](const Eigen::Ref<const
                            // RowVectorsNx2> &points) {
                            //     std::vector<SVG::PointType> _(points.rows());
                            //     Eigen::Map<RowVectorsNx2>(&_[0],
                            //     points.rows(), 2) = points; return new
                            //     SVG::Polyline(_);
                            // }), "points"_a)
                            //
        ;

    py::class_<SVG::Polygon>(m, "Polygon", py::module_local()) //
                                                               //
        ;
    py::class_<SVG::Circle>(m, "Circle", py::module_local()) //
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
