
%define	snap	20160329
%define commit	6836e17f243eebfc4a2950faee49ed3a0015b20b
%define	_ver	%(echo %{version} | tr _ -)
Summary:	SPIR-V Tools
Name:		spirv-tools
Version:	1.0_rev3.s%{snap}
Release:	1
License:	MIT-like
Group:		Applications
Source0:	https://github.com/KhronosGroup/SPIRV-Tools/archive/%{commit}/%{name}-s%{snap}.tar.gz
# Source0-md5:	3137f99a7137cfbb2aa0973d6ac5d0ff
Patch0:		cmake-lib64.patch
Patch1:		no-git-describe.patch
URL:		https://github.com/KhronosGroup/SPIRV-Tools
BuildRequires:	cmake
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SPIR-V Tools project provides an API and commands for processing
SPIR-V modules.

The project includes an assembler, binary module parser, disassembler,
and validator for SPIR-V, all based on a common static library. The
library contains all of the implementation details, and is used in the
standalone tools whilst also enabling integration into other code
bases directly.

The interfaces are still under development, and are expected to
change.

SPIR-V is defined by the Khronos Group Inc.

%package libs
Summary:	SPIR-V Tools library
Group:		Libraries

%description libs
The SPIR-V Tools project provides an API for processing SPIR-V
modules.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q -n SPIRV-Tools-%{commit}

%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake \
	../

# we know better than utils/update_build_version.py
echo '"spirv-tools %{commit}\\n"' > build-version.inc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md syntax.md
%attr(755,root,root) %{_bindir}/spirv-*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSPIRV-Tools.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/spirv
%{_includedir}/spirv-tools
