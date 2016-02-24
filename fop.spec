%global pkg_name fop
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:		%{?scl_prefix}%{pkg_name}
Summary:	XSL-driven print formatter
Version:	1.1
Release:	6.14%{?dist}
# ASL 1.1:
# several files in src/java/org/apache/fop/render/awt/viewer/resources/
# rest is ASL 2.0
License:	ASL 2.0 and ASL 1.1
URL:		http://xmlgraphics.apache.org/fop
# ./create-tarball.sh %%{version}
Source0:	%{pkg_name}-%{version}-clean.tar.gz
Source1:	%{pkg_name}.script
Source2:	batik-pdf-MANIFEST.MF
Source3:	http://mirrors.ibiblio.org/pub/mirrors/maven2/org/apache/xmlgraphics/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
Source4:	http://www.apache.org/licenses/LICENSE-1.1.txt
Source5:	create-tarball.sh
Patch0:		%{pkg_name}-main.patch
Patch1:		%{pkg_name}-Use-sRGB.icc-color-profile-from-icc-profiles-openicc.patch

BuildArch:	noarch

Requires:	%{?scl_prefix}xmlgraphics-commons >= 1.5
Requires:	%{?scl_prefix}avalon-framework >= 4.1.4
Requires:	%{?scl_prefix_java_common}batik >= 1.7
Requires:	%{?scl_prefix_java_common}xalan-j2 >= 2.7.0
Requires:	%{?scl_prefix_java_common}xml-commons-apis >= 1.3.04
Requires:	%{?scl_prefix_java_common}jakarta-commons-httpclient
Requires:	%{?scl_prefix_java_common}apache-commons-io >= 1.2
Requires:	%{?scl_prefix_java_common}apache-commons-logging >= 1.0.4
Requires:	%{?scl_prefix}icc-profiles-openicc

BuildRequires:	%{?scl_prefix_java_common}ant
BuildRequires:	%{?scl_prefix_java_common}apache-commons-logging
BuildRequires:	%{?scl_prefix_java_common}apache-commons-io
BuildRequires:	%{?scl_prefix}avalon-framework
BuildRequires:	%{?scl_prefix}xmlgraphics-commons >= 1.5
BuildRequires:	%{?scl_prefix_java_common}batik
BuildRequires:	%{?scl_prefix_java_common}tomcat-servlet-3.0-api
BuildRequires:	%{?scl_prefix_java_common}qdox
BuildRequires:	%{?scl_prefix}xmlunit
BuildRequires:	zip
BuildRequires:	%{?scl_prefix_java_common}junit

%description
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%package javadoc
Summary:	Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p0
%patch1 -p1

cp %{SOURCE4} LICENSE-1.1

sed -i -e "s|1.4|1.5|g" build.xml

#upstream workaround -- many thanks to spepping@apache.org -- see https://issues.apache.org/bugzilla/show_bug.cgi?id=50575
ln -s %{_javadir_java_common}/qdox.jar lib/build/qdox.jar
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
#qdox intentionally left off classpath -- see https://issues.apache.org/bugzilla/show_bug.cgi?id=50575
export CLASSPATH=$(build-classpath apache-commons-logging apache-commons-io xmlgraphics-commons batik-all avalon-framework-api avalon-framework-impl tomcat-servlet-3.0-api batik/batik-svg-dom xml-commons-apis xml-commons-apis-ext objectweb-asm/asm-all xmlunit)
ant jar-main transcoder-pkg javadocs
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# inject OSGi manifests
install -d -m 755 META-INF
install -p -m 644 %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{pkg_name}.jar META-INF/MANIFEST.MF

# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 build/%{pkg_name}.jar %{buildroot}%{_javadir}/%{pkg_name}.jar
install -p -m 644 build/%{pkg_name}-transcoder.jar %{buildroot}%{_javadir}/pdf-transcoder.jar

# script
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/fop

# data
install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/conf
cp -rp conf/* %{buildroot}%{_datadir}/%{pkg_name}/conf

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp build/javadocs/* %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE LICENSE-1.1 README NOTICE
%{_datadir}/%{pkg_name}
%{_javadir}/pdf-transcoder.jar
%{_bindir}/fop

%files javadoc
%doc %{_javadocdir}/%{name}
%doc LICENSE LICENSE-1.1


%changelog
* Fri Jan 29 2016 Michal Srb <msrb@redhat.com> - 1.1-6.14
- Adapt patch to rh-maven33 collection

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.1-6.13
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.1-6.12
- maven33 rebuild

* Fri Jan 16 2015 Michal Srb <msrb@redhat.com> - 1.1-6.11
- Fix path to ICC color profile

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.10
- Fix path to qdox.jar

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.1-6.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 1.1-6.9
- Fix BR/R

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.1-6.8
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.1-6.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.4
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.3
- Remove requires on java

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1-6
- Mass rebuild 2013-12-27

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 1.1-5
- Add create-tarball.sh script to SRPM

* Tue Jul 02 2013 Michal Srb <msrb@redhat.com> - 1.1-4
- Fix license tag (Resolves: rhbz#979394)
- Add ASL 1.1 license text

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Jun 21 2013 Michal Srb <msrb@redhat.com> - 1.1-2
- Build from clean tarball
- Spec file clean up

* Fri Apr 12 2013 Michal Srb <msrb@redhat.com> - 1.1-1
- Update to upstream version 1.1
- Replace proprietary color profile with free CP from icc-profiles-openicc package
- Resolves: rhbz#848659

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-20
- Add xml-commons-apis-ext to classpath

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Rüdiger Landmann <r.landmann@redhat.com> 1.0-16
- Supply missing event-model.xml files

* Fri Jun 3 2011 Rüdiger Landmann <r.landmann@redhat.com> 1.0-15
- Split avalon-framework into avalon-framework-api and avalon-framework-impl in classpath

* Thu Mar 10 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-14
- Reapply Fedora guidelines.
- Re-add pom.xml to unbreak Maven stack.
- Re-add OSGi manifest to unbreak Eclipse stack.
- Remove all bundled jars and classes and fix the build to work with our libs.

* Thu Mar 10 2011 Rüdiger Landmann <r.landmann@redhat.com> 1.0-13
- reinstate updated manifest patch
- change define to global

* Thu Mar 10 2011 Rüdiger Landmann <r.landmann@redhat.com> 1.0-12
- buildarch: noarch

* Thu Mar 10 2011 Rüdiger Landmann <r.landmann@redhat.com> 1.0-11
- drop obsolete manifest patch

* Wed Mar 10 2011 Rüdiger Landmann <r.landmann@redhat.com> 1.0-10
- import 1.0 into Fedora, based on Mandriva package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 4 2011 Rüdiger Landmann <r.landmann@redhat.com> - 1.0-8
- BR qdox

* Tue Jan 4 2011 Rüdiger Landmann <r.landmann@redhat.com> - 1.0-7
- set BR on xmlgraphics-commons >= 1.4
- Add qdox classpath

* Thu Dec 09 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.0-0.0.3mdv2011.0
- Revision: 617684
- Resubmit after moving

* Fri Dec 3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-6
- Add LICENSE to javadoc sub-package
- Few other tweaks according to new guidelines
- Make jars and javadoc versionless
- Add pom file (Resolves rhbz#655804)

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-5
- We need servlet not jsp.

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-4
- BR jsp.

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-3
- Add more BRs.

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-2
- BR ant-nodeps.

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-1
- Update to 1.0.
- BR/R java 1.6.0 not openjdk (rhbz#620330).
- Remove jars in prep.

* Sat Sep 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0-0.0.2mdv2011.0
- Revision: 576002
- rebuild for new xmlgraphics-commons

* Sun Aug 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0-0.0.1mdv2011.0
- Revision: 574030
- update to new version 1.0
- disable patch 1
- disable gcj support

* Thu Apr 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.95-0.0.3mdv2010.1
- Revision: 540954
- rebuild

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.95-0.0.2mdv2010.0
- Revision: 437573
- rebuild

* Wed Dec 17 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.95-0.0.1mdv2009.1
- Revision: 315376
- update to new version 0.95
- drop patch0, not needed anymore
- spec file clean
- drop useles buildrequires
- use %%java_home

* Sat Dec 29 2007 David Walluck <walluck@mandriva.org> 0.94-0.2.1mdv2008.1
- Revision: 139372
- spec cleanup
- import fop


* Fri Dec  7 2007 Lillian Angel <langel at redhat.com> - 0.94-2
- Updated Release.

* Thu Dec  6 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Removed ppc/64 conditions since IcedTea is now available for ppc/64.

* Tue Nov 27 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Fixed to build with gcj on ppc/64.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Fixed rpmlint errors.

* Tue Sep 18 2007 Joshua Sumali <jsumali at redhat.com> - 0:0.94-1
- Update to fop 0.94

* Thu Mar 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-9jpp
- First build for JPP-1.7
- Replace avalon-framework, avalon-logkit with their new excalibur-*
  counterparts
- Drop non-free jimi and jai BRs

* Tue Oct 11 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-8jpp
- Patch to Batik >= 1.5.1

* Fri Oct 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-7jpp
- Omit ant -d flag

* Mon Aug 23 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-6jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-5jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:0.20.5-4jpp
- Upgrade to Ant 1.6.X

* Thu Jan  8 2004 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-3jpp
- BuildRequires ant-optional.
- Crosslink with full J2SE javadocs instead of just JAXP/XML-commons.
- Add Main-Class back to manifest.

* Tue Sep 23 2003 Paul Nasrat <pauln at truemesh.com> - 0:0.20.5-2jpp
- Fix script and requires
- Remove class path in manifest
- New javadoc style

* Sat Jul 19 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-1jpp
- Update to 0.20.5.
- Crosslink with xml-commons-apis and batik javadocs.
- BuildRequires jai, jce and jimi.

* Sat Jun  7 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-0.rc3a.1jpp
- Update to 0.20.5rc3a.
- Include fop script.
- Non-versioned javadoc symlinks.

* Thu Apr 17 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-0.rc2.1jpp
- Update to 0.20.5rc2 and JPackage 1.5.

* Sun Mar 10 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.3-1jpp
- 0.20.3 final
- fixed missing symlink

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.3-0.rc.1jpp
- 0.20.3rc
- first unified release
- javadoc into javadoc package
- no dependencies for manual package
- s/jPackage/JPackage
- adaptation to new xalan-j2 package
- requires and buildrequires avalon-logkit

* Thu Aug 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.1-1mdk
- first release
