Name:           obs-studio-plugin-distroav
Version:        6.1.1
Release:        2%{?dist}
Summary:        Network Audio/Video in OBS-Studio using NDI technology

License:        GPL-2.0-or-later
URL:            https://github.com/DistroAV/DistroAV
Source0:        %{url}/archive/%{version}/DistroAV-%{version}.tar.gz

# NDI only exists on theses arches
ExclusiveArch:  i686 x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  glslc
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(vulkanloader)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  obs-studio-devel
Requires:       obs-studio%{?_isa}
Supplements:    obs-studio%{?_isa}

# This is a mandatory requirement, hence in rpmfusion-nonfree
# Version is often modeled after the ndi-sdk version
Requires:       ndi-sdk >= %{version}-1

# Old name
Obsoletes:  obs-ndi < %{version}-%{release}
Provides: obs-ndi = %{version}-%{release}


%description
Network Audio/Video in OBS-Studio using NDI technology.


%prep
%autosetup -p1 -n DistroAV-%{version}

# Where to find the libndi.so.6 library
sed -i -e 's|/usr/lib|%{_libdir}|' src/plugin-main.cpp
sed -i -e 's|/usr/local/lib|/usr/local/%{_lib}|' src/plugin-main.cpp


%build
%cmake \
  -DENABLE_FRONTEND_API=on \
  -DENABLE_QT=on

# Hack Werror
sed -i -e 's/ -Werror$//' %{__cmake_builddir}/CMakeFiles/plugin-support.dir/flags.make
sed -i -e 's/ -Werror$//' %{__cmake_builddir}/CMakeFiles/distroav.dir/flags.make

%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_libdir}/obs-plugins/distroav.so
%{_datadir}/obs/obs-plugins/distroav



%changelog
* Wed Dec 31 2025 Sérgio Basto <sergio@serjux.com> - 6.1.1-2
- Initial commit for nvidia-settings-580xx

* Mon Jun 23 2025 Nicolas Chauvet <kwizart@gmail.com> - 6.1.1-1
- Initial spec file
