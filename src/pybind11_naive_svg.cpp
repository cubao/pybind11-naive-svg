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

namespace cubao
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

CUBAO_INLINE void bind_naive_svg(py::module &m)
{
}
} // namespace cubao
