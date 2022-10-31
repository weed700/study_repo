### lustre build를 위한 사전 필요 요소

* \# yum install libtool

  * libtool를 설치하면 autoconf, automake 자동으로 설치됨

* Autotools

  * autoconf, automake, libtool 도구들로 구성되어 있는 build system
  * 대부분의 GNU 프로그램들은 Autotools를 사용해 Build 환경을 구성
  * 아래와 같은 명령어로 소스 패키지를 컴파일 하고 설치할 수 있는데, 이러한 빌드 환경을 제공하는것이 Autotools의 역할
  ```console
   # ./configure
   # make
   # make install
  ```
  * ./configure : configure 스크립트는 현재 시스템에 어떤 프로그램과 라이브러리가 설치되어 있는 지를 분석해 Makefile을 생성
  * make : 실제로 소스를 컴파일 하는 명령어
  * make install : make 명령어를 통해 빌드된 바이너리와 라이브러리를 prefix(configure 스크립트의 옵션 중 하나)로 지정된 폴더에 설치하는 명령어

* confgiure.ac : autoconf 명령어의 입력으로 사용되는 파일 -> configure 스크립트를 생성
* Makefile.am : automake 명령어의 입력으로 사용되는데, automake는 Makefile.am을 기반으로 Makefile.in 파일을 생성 -> Makefile.in은 Makefile을 생성하기 위한 템플릿

* configure.ac 매크로
 
  * autoconf는 configure.ac에 따라 configure 파일을 만듬
  * automake는 makefile.am과 configure.ac에 따라 Makefile.in을 만듬


    * AC_CANOCICAL_SYSTEM : 현재 시스템에 대한 정보를 가져옴
    * AC_PROG_CC : cc가 사용 가능한지를 check
    * AC_CHECK_HEADERS : 지정하는 header file 들이 시스템에 있는지 검사 -> HAVE_NAME_H를 만들어줌
    * AC_TYPE_ : 지정한 type definnition을 확인
    * AC_SUBST : configure.ac에서 사용한 변수들이 configure시 *.in 파일에 지정한 변수를 찾아 유효값을 넣어줌
    * AC_CONFIG_FILES : 생성될 파일들을 지정함. 흔히 Makefile

### 참고 사이트

* https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=muri1004&logNo=220616423157
