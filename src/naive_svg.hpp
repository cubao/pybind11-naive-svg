#ifndef CUBAO_NAIVE_SVG_HPP
#define CUBAO_NAIVE_SVG_HPP

// upstream
// https://github.com/cubao/headers/tree/main/include/cubao/naive_svg.hpp
// migrated from https://github.com/cubao/naive-svg/blob/master/svg.hpp

#include <vector>
#include <map>
#include <string>
#include <memory>

#include <fstream>
#include <ostream>
#include <sstream>

namespace cubao
{
// https://en.wikipedia.org/wiki/Fluent_interface
// https://rapidjson.org/md_doc_tutorial.html
// https://www.tutorialspoint.com/what-is-function-chaining-in-javascript
#ifndef SETUP_FLUENT_API
#define SETUP_FLUENT_API(Klass, VarType, VarName)                              \
    Klass &VarName(const VarType &v)                                           \
    {                                                                          \
        VarName##_ = v;                                                        \
        return *this;                                                          \
    }                                                                          \
    VarType &VarName() { return VarName##_; }                                  \
    const VarType &VarName() const { return VarName##_; }
#endif

#ifndef SETUP_FLUENT_API_FOR_SVG_ELEMENT
#define SETUP_FLUENT_API_FOR_SVG_ELEMENT(KlassType)                            \
    SETUP_FLUENT_API(KlassType, Color, stroke)                                 \
    SETUP_FLUENT_API(KlassType, double, stroke_width)                          \
    SETUP_FLUENT_API(KlassType, Color, fill)                                   \
    SETUP_FLUENT_API(KlassType, std::string, dash_array)                       \
    SETUP_FLUENT_API(KlassType, std::string, stroke_linecap)                   \
    SETUP_FLUENT_API(KlassType, std::string, stroke_linejoin)                  \
    SETUP_FLUENT_API(KlassType, std::string, transform)                        \
    SETUP_FLUENT_API(KlassType, std::string, attrs)
#endif

struct SVG
{
    using PointType = std::array<double, 2>;
    enum COLOR
    {
        RED = 0xFF0000,
        GREEN = 0x00FF00, // not css green
        BLUE = 0x0000FF,
        YELLOW = 0xFFFF00,
        WHITE = 0xFFFFFF,
        GRAY = 0x9B9B9B,
        BLACK = 0x000000,
        NONE = -1,
    };

    struct Color
    {
        Color(int rgb = -1 /* NONE */)
        {
            if (rgb >= 0) {
                r_ = (rgb >> 16) & 0xFF;
                g_ = (rgb >> 8) & 0xFF;
                b_ = rgb & 0xFF;
            }
        }
        Color(int r, int g, int b, float a = -1.f) : r_(r), g_(g), b_(b), a_(a)
        {
        }
        SETUP_FLUENT_API(Color, int, r)
        SETUP_FLUENT_API(Color, int, g)
        SETUP_FLUENT_API(Color, int, b)
        SETUP_FLUENT_API(Color, float, a)
        bool invalid() const
        {
            return r_ < 0 || g_ < 0 || b_ < 0 || //
                   r_ > 255 || g_ > 255 || b_ > 255;
        }

        friend std::ostream &operator<<(std::ostream &out, const SVG::Color &c);
        void write(std::ostream &out) const
        {
            if (invalid()) {
                out << "none";
                return;
            }
            if (0.f <= a_ && a_ <= 1.f) {
                out << "rgba(" << r_ << "," << g_ << "," << b_ << "," << a_
                    << ")";
            } else {
                out << "rgb(" << r_ << "," << g_ << "," << b_ << ")";
            }
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }
        Color clone() const { return *this; }

      private:
        int r_{-1}, g_{-1}, b_{-1};
        float a_{-1.f};
    };

    enum ELEMENT
    {
        POLYLINE,
        POLYGON,
        CIRCLE,
        TEXT,
        PATH,
        RECT
    };

    struct Element
    {
      protected:
        std::vector<PointType> points_;
        Color stroke_{COLOR::BLACK};
        double stroke_width_{1.0};
        Color fill_{COLOR::NONE};
        std::string dash_array_;
        std::string stroke_linecap_;
        std::string stroke_linejoin_;
        std::string transform_;
        std::string attrs_;

        // Helper to write common style attributes
        void write_style(std::ostream &out) const
        {
            out << " style='stroke:" << stroke_      //
                << ";stroke-width:" << stroke_width_ //
                << ";fill:" << fill_;
            if (!dash_array_.empty()) {
                out << ";stroke-dasharray:" << dash_array_;
            }
            if (!stroke_linecap_.empty()) {
                out << ";stroke-linecap:" << stroke_linecap_;
            }
            if (!stroke_linejoin_.empty()) {
                out << ";stroke-linejoin:" << stroke_linejoin_;
            }
            out << "'";
            if (!transform_.empty()) {
                out << " transform='" << transform_ << "'";
            }
        }
    };

    struct Polyline : Element
    {
        Polyline(const std::vector<PointType> &points) { points_ = points; }
        SETUP_FLUENT_API(Polyline, std::vector<SVG::PointType>, points)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Polyline)

        friend std::ostream &operator<<(std::ostream &out,
                                        const SVG::Polyline &e);
        void write(std::ostream &out) const
        {
            out << "<polyline";
            write_style(out);
            out << " points='";
            for (auto &pt : points_) {
                out << pt[0] << "," << pt[1] << " ";
            }
            out << "'";
            if (!attrs_.empty()) {
                out << " " << attrs_;
            }
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        Polyline clone() const { return *this; }
    };

    struct Polygon : Element
    {
        Polygon(const std::vector<PointType> &points) { points_ = points; }
        SETUP_FLUENT_API(Polygon, std::vector<SVG::PointType>, points)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Polygon)

        friend std::ostream &operator<<(std::ostream &out, const Polygon &e);
        void write(std::ostream &out) const
        {
            out << "<polygon";
            write_style(out);
            out << " points='";
            for (auto &pt : points_) {
                out << pt[0] << "," << pt[1] << " ";
            }
            out << "'";
            if (!attrs_.empty()) {
                out << " " << attrs_;
            }
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        Polygon clone() const { return *this; }
    };

    struct Circle : Element
    {
        Circle(const PointType &center, double r = 1.0)
        {
            points_ = {center};
            r_ = r;
        }
        Circle &center(const PointType &center)
        {
            points_[0] = center;
            return *this;
        }
        PointType &center() { return points_[0]; }
        const PointType &center() const { return points_[0]; }
        Circle &x(double x)
        {
            points_[0][0] = x;
            return *this;
        }
        double &x() { return points_[0][0]; }
        const double &x() const { return points_[0][0]; }
        Circle &y(double y)
        {
            points_[0][1] = y;
            return *this;
        }
        double &y() { return points_[0][1]; }
        const double &y() const { return points_[0][1]; }

        SETUP_FLUENT_API(Circle, double, r)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Circle)

        friend std::ostream &operator<<(std::ostream &out,
                                        const SVG::Circle &e);
        void write(std::ostream &out) const
        {
            out << "<circle r='" << r_ << "'" //
                << " cx='" << x() << "' cy='" << y() << "'";
            write_style(out);
            if (!attrs_.empty()) {
                out << " " << attrs_;
            }
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        Circle clone() const { return *this; }

      protected:
        double r_{1.0};
    };

    struct Text : Element
    {
        Text(const PointType &position, const std::string &text,
             int fontsize = 10.0)
        {
            points_ = {position};
            text_ = text;
            fontsize_ = fontsize;
            fill_ = COLOR::BLACK;
        }
        Text &position(const PointType &p)
        {
            points_[0] = p;
            return *this;
        }
        PointType &position() { return points_[0]; }
        const PointType &position() const { return points_[0]; }

        Text &x(double x)
        {
            points_[0][0] = x;
            return *this;
        }
        double &x() { return points_[0][0]; }
        const double &x() const { return points_[0][0]; }
        Text &y(double y)
        {
            points_[0][1] = y;
            return *this;
        }
        double &y() { return points_[0][1]; }
        const double &y() const { return points_[0][1]; }

        SETUP_FLUENT_API(Text, std::string, text)
        SETUP_FLUENT_API(Text, std::vector<std::string>, lines)
        SETUP_FLUENT_API(Text, double, fontsize)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Text)

        friend std::ostream &operator<<(std::ostream &out, const SVG::Text &e);

        void write(std::ostream &out) const
        {
            out << "<text"                                //
                << " x='" << x() << "' y='" << y() << "'" //
                << " fill='" << fill_ << "'"              //
                << " font-size='" << fontsize_ << "'"     //
                << " font-family='monospace'";
            if (!attrs_.empty()) {
                out << " " << attrs_;
            }
            out << ">" << html_escape(text_);
            if (!lines_.empty()) {
                double fontsize = fontsize_ / 5.0;
                for (auto &line : lines_) {
                    out << "<tspan xml:space='preserve' x='" << x() //
                        << "' dy='" << fontsize                     //
                        << "' fill='" << fill_                      //
                        << "' font-size='" << fontsize              //
                        << "' font-family='monospace'>"             //
                        << html_escape(line) << "</tspan>";
                }
            }
            out << "</text>";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        Text clone() const { return *this; }

        static std::string html_escape(const std::string &text)
        {
            std::string buffer;
            for (char c : text) {
                switch (c) {
                case '&':
                    buffer.append("&amp;");
                    break;
                case '\"':
                    buffer.append("&quot;");
                    break;
                case '\'':
                    buffer.append("&apos;");
                    break;
                case '<':
                    buffer.append("&lt;");
                    break;
                case '>':
                    buffer.append("&gt;");
                    break;
                default:
                    buffer.push_back(c);
                    break;
                }
            }
            return buffer;
        }

      protected:
        std::string text_;
        std::vector<std::string> lines_;
        double fontsize_{10.0};
    };

    struct Path : Element
    {
        Path(const std::string &d = "") : d_(d) {}
        SETUP_FLUENT_API(Path, std::string, d)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Path)

        // Convenience methods for building path data
        Path &move_to(double x, double y)
        {
            if (!d_.empty())
                d_ += " ";
            d_ += "M " + std::to_string(x) + " " + std::to_string(y);
            return *this;
        }
        Path &line_to(double x, double y)
        {
            if (!d_.empty())
                d_ += " ";
            d_ += "L " + std::to_string(x) + " " + std::to_string(y);
            return *this;
        }
        Path &close()
        {
            if (!d_.empty())
                d_ += " ";
            d_ += "Z";
            return *this;
        }
        Path &quadratic(double cx, double cy, double x, double y)
        {
            if (!d_.empty())
                d_ += " ";
            d_ += "Q " + std::to_string(cx) + " " + std::to_string(cy) + " " +
                  std::to_string(x) + " " + std::to_string(y);
            return *this;
        }
        Path &cubic(double c1x, double c1y, double c2x, double c2y, double x,
                    double y)
        {
            if (!d_.empty())
                d_ += " ";
            d_ += "C " + std::to_string(c1x) + " " + std::to_string(c1y) + " " +
                  std::to_string(c2x) + " " + std::to_string(c2y) + " " +
                  std::to_string(x) + " " + std::to_string(y);
            return *this;
        }
        Path &arc(double rx, double ry, double x_axis_rotation,
                  int large_arc_flag, int sweep_flag, double x, double y)
        {
            if (!d_.empty())
                d_ += " ";
            d_ += "A " + std::to_string(rx) + " " + std::to_string(ry) + " " +
                  std::to_string(x_axis_rotation) + " " +
                  std::to_string(large_arc_flag) + " " +
                  std::to_string(sweep_flag) + " " + std::to_string(x) + " " +
                  std::to_string(y);
            return *this;
        }

        friend std::ostream &operator<<(std::ostream &out, const SVG::Path &e);
        void write(std::ostream &out) const
        {
            out << "<path d='" << d_ << "'";
            write_style(out);
            if (!attrs_.empty()) {
                out << " " << attrs_;
            }
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        Path clone() const { return *this; }

      protected:
        std::string d_;
    };

    struct Rect : Element
    {
        Rect(double x = 0, double y = 0, double width = 0, double height = 0)
            : x_(x), y_(y), width_(width), height_(height)
        {
        }
        SETUP_FLUENT_API(Rect, double, x)
        SETUP_FLUENT_API(Rect, double, y)
        SETUP_FLUENT_API(Rect, double, width)
        SETUP_FLUENT_API(Rect, double, height)
        SETUP_FLUENT_API(Rect, double, rx)
        SETUP_FLUENT_API(Rect, double, ry)
        SETUP_FLUENT_API_FOR_SVG_ELEMENT(Rect)

        friend std::ostream &operator<<(std::ostream &out, const SVG::Rect &e);
        void write(std::ostream &out) const
        {
            out << "<rect x='" << x_ << "' y='" << y_ << "'"
                << " width='" << width_ << "' height='" << height_ << "'";
            if (rx_ > 0) {
                out << " rx='" << rx_ << "'";
            }
            if (ry_ > 0) {
                out << " ry='" << ry_ << "'";
            }
            write_style(out);
            if (!attrs_.empty()) {
                out << " " << attrs_;
            }
            out << " />";
        }
        std::string to_string() const
        {
            std::stringstream ss;
            write(ss);
            return ss.str();
        }

        Rect clone() const { return *this; }

      protected:
        double x_{0}, y_{0}, width_{0}, height_{0};
        double rx_{0}, ry_{0};
    };

    SVG(double width, double height) : width_(width), height_(height) {}
    ~SVG()
    {
        for (auto &pair : elements_) {
            const auto type = pair.first;
            if (type == ELEMENT::POLYGON) {
                delete (Polygon *)pair.second;
            } else if (type == ELEMENT::POLYLINE) {
                delete (Polyline *)pair.second;
            } else if (type == ELEMENT::CIRCLE) {
                delete (Circle *)pair.second;
            } else if (type == ELEMENT::TEXT) {
                delete (Text *)pair.second;
            } else if (type == ELEMENT::PATH) {
                delete (Path *)pair.second;
            } else if (type == ELEMENT::RECT) {
                delete (Rect *)pair.second;
            }
        }
    }

    // disable shallow copy
  private:
    SVG(const SVG &) = default;
    SVG &operator=(const SVG &) = default;
    SVG(SVG &&) = delete;
    SVG &operator=(SVG &&) = delete;
    // implement deep copy
  public:
    std::unique_ptr<SVG> clone() const
    {
        // auto ptr = std::make_unique<SVG>(*this);
        std::unique_ptr<SVG> ptr(new SVG(*this));
        for (auto &pair : elements_) {
            const auto type = pair.first;
            if (type == ELEMENT::POLYGON) {
                ptr->add(*(Polygon *)pair.second);
            } else if (type == ELEMENT::POLYLINE) {
                ptr->add(*(Polyline *)pair.second);
            } else if (type == ELEMENT::CIRCLE) {
                ptr->add(*(Circle *)pair.second);
            } else if (type == ELEMENT::TEXT) {
                ptr->add(*(Text *)pair.second);
            } else if (type == ELEMENT::PATH) {
                ptr->add(*(Path *)pair.second);
            } else if (type == ELEMENT::RECT) {
                ptr->add(*(Rect *)pair.second);
            }
        }
        return ptr;
    }

    SETUP_FLUENT_API(SVG, double, width)
    SETUP_FLUENT_API(SVG, double, height)
    SETUP_FLUENT_API(SVG, std::vector<double>, view_box)
    SETUP_FLUENT_API(SVG, double, grid_step)
    SETUP_FLUENT_API(SVG, std::vector<double>, grid_x)
    SETUP_FLUENT_API(SVG, std::vector<double>, grid_y)
    SETUP_FLUENT_API(SVG, Color, grid_color)
    SETUP_FLUENT_API(SVG, Color, background)
    SETUP_FLUENT_API(SVG, std::string, attrs)

    Polyline &add(const Polyline &polyline)
    {
        auto ptr = new Polyline({});
        *ptr = polyline;
        elements_.push_back({ELEMENT::POLYLINE, (void *)ptr});
        return *ptr;
    }
    Polygon &add(const Polygon &polygon)
    {
        auto ptr = new Polygon({});
        *ptr = polygon;
        elements_.push_back({ELEMENT::POLYGON, (void *)ptr});
        return *ptr;
    }
    Circle &add(const Circle &circle)
    {
        auto ptr = new Circle(circle.center());
        *ptr = circle;
        elements_.push_back({ELEMENT::CIRCLE, (void *)ptr});
        return *ptr;
    }
    Text &add(const Text &text)
    {
        auto ptr = new Text(text.position(), "");
        *ptr = text;
        elements_.push_back({ELEMENT::TEXT, (void *)ptr});
        return *ptr;
    }
    Path &add(const Path &path)
    {
        auto ptr = new Path();
        *ptr = path;
        elements_.push_back({ELEMENT::PATH, (void *)ptr});
        return *ptr;
    }
    Rect &add(const Rect &rect)
    {
        auto ptr = new Rect();
        *ptr = rect;
        elements_.push_back({ELEMENT::RECT, (void *)ptr});
        return *ptr;
    }

    Polyline &add_polyline(const std::vector<PointType> &points)
    {
        auto ptr = new Polyline(points);
        elements_.push_back({ELEMENT::POLYLINE, (void *)ptr});
        return *ptr;
    }

    Polygon &add_polygon(const std::vector<PointType> &points)
    {
        auto ptr = new Polygon(points);
        elements_.push_back({ELEMENT::POLYGON, (void *)ptr});
        return *ptr;
    }

    Circle &add_circle(const PointType &center, double r = 1.0)
    {
        auto ptr = new Circle(center, r);
        elements_.push_back({ELEMENT::CIRCLE, (void *)ptr});
        return *ptr;
    }

    Text &add_text(const PointType &position, const std::string &text,
                   int fontsize = 10.0)
    {
        auto ptr = new Text(position, text, fontsize);
        elements_.push_back({ELEMENT::TEXT, (void *)ptr});
        return *ptr;
    }

    Path &add_path(const std::string &d = "")
    {
        auto ptr = new Path(d);
        elements_.push_back({ELEMENT::PATH, (void *)ptr});
        return *ptr;
    }

    Rect &add_rect(double x, double y, double width, double height)
    {
        auto ptr = new Rect(x, y, width, height);
        elements_.push_back({ELEMENT::RECT, (void *)ptr});
        return *ptr;
    }

    size_t num_elements() const { return elements_.size(); }

    bool empty() const { return elements_.empty(); }

    void pop()
    {
        if (elements_.empty()) {
            return;
        }
        auto del = elements_.back();
        elements_.pop_back();
        if (del.first == ELEMENT::POLYLINE) {
            delete (Polyline *)del.second;
        } else if (del.first == ELEMENT::POLYGON) {
            delete (Polygon *)del.second;
        } else if (del.first == ELEMENT::CIRCLE) {
            delete (Circle *)del.second;
        } else if (del.first == ELEMENT::TEXT) {
            delete (Text *)del.second;
        } else if (del.first == ELEMENT::PATH) {
            delete (Path *)del.second;
        } else if (del.first == ELEMENT::RECT) {
            delete (Rect *)del.second;
        }
    }

    bool is_polyline(int index) const
    {
        index = __index(index);
        if (index < 0) {
            return false;
        }
        return elements_.at(index).first == ELEMENT::POLYLINE;
    }
    bool is_polygon(int index) const
    {
        index = __index(index);
        if (index < 0) {
            return false;
        }
        return elements_.at(index).first == ELEMENT::POLYGON;
    }
    bool is_circle(int index) const
    {
        index = __index(index);
        if (index < 0) {
            return false;
        }
        return elements_.at(index).first == ELEMENT::CIRCLE;
    }
    bool is_text(int index) const
    {
        index = __index(index);
        if (index < 0) {
            return false;
        }
        return elements_.at(index).first == ELEMENT::TEXT;
    }
    bool is_path(int index) const
    {
        index = __index(index);
        if (index < 0) {
            return false;
        }
        return elements_.at(index).first == ELEMENT::PATH;
    }
    bool is_rect(int index) const
    {
        index = __index(index);
        if (index < 0) {
            return false;
        }
        return elements_.at(index).first == ELEMENT::RECT;
    }

    Polyline *as_polyline(int index)
    {
        if (!is_polyline(index)) {
            return nullptr;
        }
        return (Polyline *)elements_.at(index % elements_.size()).second;
    }
    Polygon *as_polygon(int index)
    {
        if (!is_polygon(index)) {
            return nullptr;
        }
        return (Polygon *)elements_.at(index % elements_.size()).second;
    }
    Circle *as_circle(int index)
    {
        if (!is_circle(index)) {
            return nullptr;
        }
        return (Circle *)elements_.at(index % elements_.size()).second;
    }
    Text *as_text(int index)
    {
        if (!is_text(index)) {
            return nullptr;
        }
        return (Text *)elements_.at(index % elements_.size()).second;
    }
    Path *as_path(int index)
    {
        if (!is_path(index)) {
            return nullptr;
        }
        return (Path *)elements_.at(index % elements_.size()).second;
    }
    Rect *as_rect(int index)
    {
        if (!is_rect(index)) {
            return nullptr;
        }
        return (Rect *)elements_.at(index % elements_.size()).second;
    }
    // const version
    const Polyline *as_polyline(int index) const
    {
        return const_cast<const Polyline *>(
            const_cast<SVG *>(this)->as_polyline(index));
    }
    const Polygon *as_polygon(int index) const
    {
        return const_cast<const Polygon *>(
            const_cast<SVG *>(this)->as_polygon(index));
    }
    const Circle *as_circle(int index) const
    {
        return const_cast<const Circle *>(
            const_cast<SVG *>(this)->as_circle(index));
    }
    const Text *as_text(int index) const
    {
        return const_cast<const Text *>(
            const_cast<SVG *>(this)->as_text(index));
    }
    const Path *as_path(int index) const
    {
        return const_cast<const Path *>(
            const_cast<SVG *>(this)->as_path(index));
    }
    const Rect *as_rect(int index) const
    {
        return const_cast<const Rect *>(
            const_cast<SVG *>(this)->as_rect(index));
    }

    void write(std::ostream &out) const
    {
        out << "<svg width='" << width_ << "' height='" << height_ << "'";
        if (view_box_.size() == 4) {
            out << " viewBox='" << view_box_[0] //
                << " " << view_box_[1]          //
                << " " << view_box_[2]          //
                << " " << view_box_[3] << "'";
        }
        out << " xmlns='http://www.w3.org/2000/svg'"
               " xmlns:xlink='http://www.w3.org/1999/xlink'";
        if (!attrs_.empty()) {
            out << " " << attrs_;
        }
        out << ">";
        if (!background_.invalid()) {
            out << "\n\t<rect width='100%' height='100%' fill='" //
                << background_                                   //
                << "'/>";
        }
        double xmin = 0.0, xmax = width_, xstep = grid_step_;
        double ymin = 0.0, ymax = height_, ystep = grid_step_;
        if (grid_x_.size() == 3 && grid_y_.size() == 3) {
            xmin = grid_x_[0];
            xmax = grid_x_[1];
            xstep = grid_x_[2];
            ymin = grid_y_[0];
            ymax = grid_y_[1];
            ystep = grid_y_[2];
        }
        if (xstep > 0 && ystep > 0 && xmin < xmax && ymin < ymax) {
            SVG::Color grid_color = SVG::COLOR::GRAY;
            if (!grid_color_.invalid()) {
                grid_color = grid_color_;
            }
            for (double x = xmin; x <= xmax; x += xstep) {
                out << "\n\t"
                    << SVG::Polyline({{x, ymin}, {x, ymax}}).stroke(grid_color);
            }
            for (double y = ymin; y <= ymax; y += ystep) {
                out << "\n\t"
                    << SVG::Polyline({{xmin, y}, {xmax, y}}).stroke(grid_color);
            }
        }
        for (auto &pair : elements_) {
            out << "\n\t";
            if (pair.first == ELEMENT::POLYGON) {
                ((Polygon *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::POLYLINE) {
                ((Polyline *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::CIRCLE) {
                ((Circle *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::TEXT) {
                ((Text *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::PATH) {
                ((Path *)pair.second)->write(out);
            } else if (pair.first == ELEMENT::RECT) {
                ((Rect *)pair.second)->write(out);
            }
        }
        out << "\n</svg>";
    }

    std::string to_string() const
    {
        std::stringstream ss;
        write(ss);
        return ss.str();
    }

    void dump(const std::string &path) const
    {
        std::ofstream file(path);
        write(file);
        file.close();
    }

  private:
    // size
    double width_, height_;
    // viewBox
    std::vector<double> view_box_;
    // grid
    double grid_step_{-1.0};
    std::vector<double> grid_x_, grid_y_; // low, high, step
    Color grid_color_{COLOR::GRAY};
    // background
    Color background_{COLOR::NONE};
    // attrs
    std::string attrs_;
    // elements
    std::vector<std::pair<ELEMENT, void *>> elements_;

    int __index(int index) const
    {
        if (index < 0) {
            index += elements_.size();
        }
        if (0 <= index && index < (int)elements_.size()) {
            return index;
        }
        return -1;
    }
};

inline std::ostream &operator<<(std::ostream &out, const SVG::Color &c)
{
    c.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Polyline &p)
{
    p.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Polygon &p)
{
    p.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Circle &c)
{
    c.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Text &t)
{
    t.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Path &p)
{
    p.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG::Rect &r)
{
    r.write(out);
    return out;
}

inline std::ostream &operator<<(std::ostream &out, const SVG &s)
{
    s.write(out);
    return out;
}

} // namespace cubao

#undef SETUP_FLUENT_API
#undef SETUP_FLUENT_API_FOR_SVG_ELEMENT

#endif
