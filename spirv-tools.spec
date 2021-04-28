Summary:	Khronos SPIR-V Tools
Summary(pl.UTF-8):	Narzędzia SPIR-V z projektu Khronos
Name:		spirv-tools
Version:	2020.6
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Development/Tools
#Source0Download: https://github.com/KhronosGroup/SPIRV-Tools/releases
Source0:	https://github.com/KhronosGroup/SPIRV-Tools/archive/v%{version}/SPIRV-Tools-%{version}.tar.gz
# Source0-md5:	a5e7b94edc9f8ecc798c66a549bba181
Patch0:		no-git-describe.patch
URL:		https://github.com/KhronosGroup/SPIRV-Tools
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	python3 >= 1:3
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	spirv-headers >= 1.5.4-2
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SPIR-V Tools project provides an API and commands for processing
SPIR-V modules.

The project includes an assembler, binary module parser, disassembler,
and validator for SPIR-V, all based on a common library. The library
contains all of the implementation details, and is used in the
standalone tools whilst also enabling integration into other code
bases directly.

The interfaces are still under development, and are expected to
change.

SPIR-V is defined by the Khronos Group Inc.

%description -l pl.UTF-8
SPIR-V Tools to projekt udostępniający API i polecenia do
przetwarzania modułów SPIR-V.

Projekt zawiera asembler, parser modułów binarnych, disasembler oraz
walidator dla SPIR-V - wszystko oparte o wspólną bibliotekę.
Biblioteka zawiera wszystkie szczegóły implementacji i jest używana w
samodzielnych narzędziach; może być także zintegrowana do innego kodu.

Interfejsy są nadal rozwijane i mogą się zmienić.

SPIR-V jest zdefiniowane przez Khronos Group Inc.

%package libs
Summary:	SPIR-V Tools library
Summary(pl.UTF-8):	Biblioteka SPIR-V Tools
Group:		Libraries

%description libs
The SPIR-V Tools project provides an API for processing SPIR-V
modules.

%description libs -l pl.UTF-8
Projekt SPIR-V Tools udostepnia API do przetwarzania modułów SPIR-V.

%package devel
Summary:	Header files for SPIR-V Tools library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SPIR-V Tools
Group:		Development/Libraries
Requires:	spirv-headers >= 1.5.4-2
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files for SPIR-V Tools library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SPIR-V Tools.

%prep
%setup -q -n SPIRV-Tools-%{version}
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env sh,/bin/sh,' tools/lesspipe/spirv-lesspipe.sh

%build
install -d build

cd build
# .pc file generation expects relative CMAKE_INSTALL_*DIR
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DSPIRV-Headers_SOURCE_DIR=/usr \
	-DSPIRV_TOOLS_BUILD_STATIC=OFF \
	-DSPIRV_WERROR=OFF

# we know better than utils/update_build_version.py
echo '"spirv-tools %{version}\\n"' > build-version.inc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README.md docs/syntax.md
%attr(755,root,root) %{_bindir}/spirv-as
%attr(755,root,root) %{_bindir}/spirv-cfg
%attr(755,root,root) %{_bindir}/spirv-dis
%attr(755,root,root) %{_bindir}/spirv-lesspipe.sh
%attr(755,root,root) %{_bindir}/spirv-link
%attr(755,root,root) %{_bindir}/spirv-opt
%attr(755,root,root) %{_bindir}/spirv-reduce
%attr(755,root,root) %{_bindir}/spirv-val

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSPIRV-Tools.so
%attr(755,root,root) %{_libdir}/libSPIRV-Tools-link.so
%attr(755,root,root) %{_libdir}/libSPIRV-Tools-opt.so
%attr(755,root,root) %{_libdir}/libSPIRV-Tools-reduce.so
%attr(755,root,root) %{_libdir}/libSPIRV-Tools-shared.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/spirv-tools
%{_pkgconfigdir}/SPIRV-Tools.pc
%{_pkgconfigdir}/SPIRV-Tools-shared.pc
%{_libdir}/cmake/SPIRV-Tools
%{_libdir}/cmake/SPIRV-Tools-link
%{_libdir}/cmake/SPIRV-Tools-opt
%{_libdir}/cmake/SPIRV-Tools-reduce
