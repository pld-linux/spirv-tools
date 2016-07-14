
%define	snap	20160614
%define commit	37e4600c3efad7b1cfdc1df70a977be82eb3c811
%define headers_commit	34d319db9d6cefe93191b921f5f1593378a98c4c
%define	_ver	%(echo %{version} | tr _ -)
Summary:	SPIR-V Tools
Name:		spirv-tools
Version:	1.0_rev3.s%{snap}
Release:	1
License:	MIT-like
Group:		Applications
Source0:	https://github.com/KhronosGroup/SPIRV-Tools/archive/%{commit}/%{name}-s%{snap}.tar.gz
# Source0-md5:	323d546700f9d1e72a34f77fec4bacfb
Source1:	https://github.com/KhronosGroup/SPIRV-Headers/archive/%{headers_commit}/spirv-headers-%{headers_commit}.tar.gz
# Source1-md5:	94c7722f2be6182e9cf9bc29c6034f02
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
%setup -q -n SPIRV-Tools-%{commit} -a1

mv SPIRV-Headers-* external/spirv-headers

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
install -d $RPM_BUILD_ROOT%{_includedir}/spirv

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

cp -a external/spirv-headers/include/spirv/* $RPM_BUILD_ROOT%{_includedir}/spirv

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
