%{?_javapackages_macros:%_javapackages_macros}
Name:          glassfish-toplink-essentials
Version:       2.0.46
Release:       6.0%{?dist}
Summary:       Glassfish JPA Toplink Essentials

License:       CDDL or GPLv2 with exceptions
URL:           http://glassfish.java.net/javaee5/persistence/
Source0:       http://dlc.sun.com.edgesuite.net/javaee5/promoted/source/glassfish-persistence-v2-b46-src.zip
# wget http://download.java.net/javaee5/v2.1.1_branch/promoted/source/glassfish-v2.1.1-b31g-src.zip
# unzip glassfish-v2.1.1-b31g-src.zip
# mkdir -p glassfish-bootstrap
# mv glassfish/bootstrap/* glassfish-bootstrap
# tar czf glassfish-bootstrap.tar.gz glassfish-bootstrap
Source1:       glassfish-bootstrap.tar.gz
# fix javadoc build
Patch0:        glassfish-entity-persistence-build.patch

Patch1:        glassfish-persistence-2.0.41-jdk7.patch
Patch2:        glassfish-persistence-2.0.41-agent-remove-manifest-classpath.patch
Patch3:        glassfish-persistence-2.0.41-use_system_antlr.patch

BuildRequires: java-devel
BuildRequires: jpackage-utils

BuildRequires: ant
BuildRequires: antlr-tool
BuildRequires: geronimo-jta
BuildRequires: geronimo-jpa

Requires:      antlr-tool
Requires:      geronimo-jpa
Requires:      geronimo-jta

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description
Glassfish Persistence Implementation.

%package javadoc

Summary:       Javadoc for %{name} Implementation
Requires:      jpackage-utils

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -c

tar xzf %{SOURCE1}
mv glassfish-bootstrap glassfish/bootstrap
find . -name "*.class" -delete
find . -name "*.jar" -delete

%patch0
%patch1
%patch2
%patch3

sed -i -e 's/@VERSION@/%{version}/' glassfish/entity-persistence/toplink-essentials.pom
sed -i -e 's/@VERSION@/%{version}/' glassfish/entity-persistence/toplink-essentials-agent.pom

cd glassfish/bootstrap/legal
for d in CDDLv1.0.txt LICENSE.txt COPYRIGHT 3RD-PARTY-LICENSE.txt ; do
  iconv -f iso8859-1 -t utf-8 $d > $d.conv && mv -f $d.conv $d
  sed -i 's/\r//' $d
done

%build

pushd glassfish/entity-persistence
  export CLASSPATH=$(build-classpath geronimo-jpa)
  %ant -Djavaee.jar=$(build-classpath geronimo-jta) -Dglassfish.schemas.home=$PWD/../persistence-api/schemas all docs
popd

%install

mkdir -p %{buildroot}%{_javadir}/glassfish
install -m 644 publish/glassfish/lib/toplink-essentials.jar %{buildroot}%{_javadir}/%{name}.jar
install -m 644 publish/glassfish/lib/toplink-essentials-agent.jar %{buildroot}%{_javadir}/%{name}-agent.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 glassfish/entity-persistence/toplink-essentials.pom \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar
install -pm 644 glassfish/entity-persistence/toplink-essentials-agent.pom \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}-agent.pom
%add_maven_depmap JPP-%{name}-agent.pom %{name}-agent.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr glassfish/entity-persistence/build/javadoc/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-agent.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{name}-agent.pom
%{_mavendepmapfragdir}/%{name}
%doc glassfish/bootstrap/legal/*

%files javadoc
%{_javadocdir}/%{name}
%doc glassfish/bootstrap/legal/3RD-PARTY-LICENSE*.txt
%doc glassfish/bootstrap/legal/CDDL*.txt
%doc glassfish/bootstrap/legal/COPYRIGHT
%doc glassfish/bootstrap/legal/LICENSE.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 gil cattaneo <puntogil@libero.it> 2.0.46-3
- moved in files in %%{_javadir}
- fixed Url and source0 url

* Thu Jun 28 2012 gil cattaneo <puntogil@libero.it> 2.0.46-2
- change license tag

* Thu May 24 2012 gil cattaneo <puntogil@libero.it> 2.0.46-1
- update to 2.0.46

* Fri Apr 06 2012 gil cattaneo <puntogil@libero.it> 2.0.41-1
- initial rpm