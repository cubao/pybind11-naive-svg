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

CUBAO_INLINE void bind_naive_svg(py::module &m)
{
    py::class_<SVG::Polyline>(m, "Polyline", py::module_local()) //
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
